var vumigo = require("vumigo_v01");
var jed = require("jed");

if (typeof api === "undefined") {
    // testing hook (supplies api when it is not passed in by the real sandbox)
    var api = this.api = new vumigo.dummy_api.DummyApi();
}

var Promise = vumigo.promise.Promise;
var success = vumigo.promise.success;
var Choice = vumigo.states.Choice;
var ChoiceState = vumigo.states.ChoiceState;
var FreeText = vumigo.states.FreeText;
var EndState = vumigo.states.EndState;
var BookletState = vumigo.states.BookletState;
var InteractionMachine = vumigo.state_machine.InteractionMachine;
var StateCreator = vumigo.state_machine.StateCreator;

function SMSEndState(name, text, next, handlers) {
    // State that mimicks the USSD behaviour when a USSD session ends
    // it fast forwards to the start of the InteractionMachine.
    // We need to do this because SMS doesn't have the Session capabities
    // that provide us this functionality when using USSD.
    var self = this;
    handlers = handlers || {};
    if(handlers.on_enter === undefined) {
        handlers.on_enter = function() {
            self.input_event('', function() {});
        };
    }
    EndState.call(self, name, text, next, handlers);
}

function GoNikeGHRSMSError(msg) {
    var self = this;
    self.msg = msg;

    self.toString = function() {
        return "<GoNikeGHRError: " + self.msg + ">";
    };
}

function GoNikeGHRSMS() {
    var self = this;

    self.post_headers = {
        'Content-Type': ['application/x-www-form-urlencoded']
    };

    // The first state to enter
    StateCreator.call(self, 'start');

    self.get_today = function(im) {
        if (im.config.testing) {
            return new Date(im.config.testing_mock_today[0],
                             im.config.testing_mock_today[1],
                             im.config.testing_mock_today[2],
                             im.config.testing_mock_today[3],
                             im.config.testing_mock_today[4]);
        } else {
            return new Date();
        }
    };

    self.error_state = function() {
        return new EndState(
            "end_state_error",
            "Sorry! Something went wrong. Please redial and try again.",
            "initial_state"
        );
    };

    self.get_contact = function(im){
        var p = im.api_request('contacts.get_or_create', {
            delivery_class: 'ussd',
            addr: im.user_addr
        });
        return p;
    };

    self.crm_post = function(path, data) {
        var url = im.config.crm_api_root + path + "?format=json";
        data = self.url_encode(data);
        var p = im.api_request("http.post", {
            url: url,
            headers: self.post_headers,
            data: data
        });
        p.add_callback(function(result) {
            var json = self.check_reply(result, url, 'POST', data, false);
            return json;
        });
        return p;
    };

    self.interaction_log = function(feature, key, value) {
        var data = {
            feature: feature,
            key: key,
            value: value,
            transport: 'ussd',
            msisdn: im.user_addr
        };
        return self.crm_post("userinteraction/", data);
    };

    self.url_encode = function(params) {
        var items = [];
        for (var key in params) {
            items[items.length] = (encodeURIComponent(key) + '=' +
                                   encodeURIComponent(params[key]));
        }
        return items.join('&');
    };

    self.check_reply = function(reply, url, method, data, ignore_error) {
        var error;
        if (reply.success && (reply.code >= 200 && reply.code < 300))  {
            if (reply.body) {
                var json = JSON.parse(reply.body);
                return json;
            } else {
                return null;
            }
        }
        else {
            error = reply.reason;
        }
        var error_msg = ("API " + method + " to " + url + " failed: " +
                         error);
        if (typeof data != 'undefined') {
            error_msg = error_msg + '; data: ' + JSON.stringify(data);
        }
        im.log(error_msg);
        if (!ignore_error) {
            throw new GoNikeGHRError(error_msg);
        }
    };

    self.make_thanks_state = function(state_name, text){
        return new SMSEndState(
            state_name,
            text,
            state_name);
    };

    self.clean_string = function(text) {
        var punctuation_less = text.replace(/[\.,-\/#!$%\^&\*;:{}=\-_`~()]/g,"");
        return punctuation_less.replace(/\s{2,}/g," ");
    };

    self.check_swear = function(text){
        var swear_words = im.config.swear_words;
        var swear = false;
        text = self.clean_string(text).toLowerCase().split(' ');
        for(var i=0;i<swear_words.length;i++){
            if (text.indexOf(swear_words[i]) != -1){
                swear = true;
            }
        }
        return swear;
    };


    // Creates a key like "2013-06-10_airtime"
    self.get_week_airtime_key = function() {
        var monday = self.get_monday(self.get_today(im));
        var monday_date_str = monday.toISOString().substring(0,10);
        return monday_date_str + '_airtime_committed';
    };


    self.increment_counter = function(metric_key) {
        return function(){
            return im.api_request('kv.incr', {
                key: metric_key,
                amount: 1
            });
        };
    };

    self.update_extras = function(contact_key, extras_fields) {
        return function() {
            return im.api_request('contacts.update_extras', {
                key: contact_key,
                fields: extras_fields
            });
        };
    };

    self.add_state(new FreeText(
            'start',
            'process_sms',
            "Should never be seen"
    ));

    self.add_creator('process_sms', function(state_name, im) {
        // Expects to be used on SMS channel
        var fields = {}; // We'll populate if we need to update the extras
        var content = im.get_user_answer('start');
        var today = self.get_today(im);
        var includes_swear = false;
        var is_spammer = false;
        if (content !== undefined) {
            var p = self.get_contact(im);
            p.add_callback(function(result){
                var contact = result.contact;
                var p_c = new Promise();
                // New contact metric
                if (typeof contact["extras-ghr_sms_opinion_last"] == 'undefined') {
                    p_c.add_callback(self.increment_counter("ghr_sms_total_unique_users"));
                }
                // Swearing checks
                includes_swear = self.check_swear(content);
                if(includes_swear){
                    fields['ghr_rude'] = self.get_today(im).toISOString();
                }
                // Spam checks
                if (typeof contact["extras-ghr_sms_opinion_last"] == 'undefined' || content != contact["extras-ghr_sms_opinion_last"]) {
                    // first time opinion or not same as last time
                    fields['ghr_sms_opinion_last'] = content;
                    fields['ghr_sms_opinion_first_seen'] = today.toISOString();
                    fields['ghr_sms_opinion_seen_count'] = "1";
                } else {
                    // current content is same as last
                    var seen_count = parseInt(contact["extras-ghr_sms_opinion_seen_count"])+1;
                    var first_seen = new Date(contact["extras-ghr_sms_opinion_first_seen"]);
                    var day = 1000*60*60*24;
                    if (seen_count >= 5 && (today-first_seen) < day){
                        // seen 5 or more times in last 24 hours
                        fields['ghr_spammer'] = today.toISOString();
                        is_spammer = true;
                    } else {
                        // just up the seen count - not spammer yet
                        fields['ghr_sms_opinion_seen_count'] = seen_count.toString();
                    }
                }
                p_c.add_callback(self.update_extras(contact.key, fields));
                p_c.callback();
                return p_c;
            });
            p.add_callback(function(result){
                if (includes_swear || is_spammer){
                    return self.make_thanks_state(state_name, "Thanks for your SMS opinion! " +
                        "Please try to keep messages clean!");
                } else {
                    // all clean
                    return self.make_thanks_state(state_name, "Thanks for your SMS opinion!");
                }
            });
            return p;
        } else {
            return self.make_thanks_state(state_name, "Nothing to say?");
        }

    });
};

// launch app
var states = new GoNikeGHRSMS();
var im = new InteractionMachine(api, states);
im.attach();
