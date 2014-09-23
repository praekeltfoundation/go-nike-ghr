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



function GoNikeGHRError(msg) {
    var self = this;
    self.msg = msg;

    self.toString = function() {
        return "<GoNikeGHRError: " + self.msg + ">";
    };
}

function GoNikeGHR() {
    var self = this;
    var _ = new jed({});

    self.post_headers = {
        'Content-Type': ['application/x-www-form-urlencoded']
    };

    // The first state to enter

    StateCreator.call(self, 'initial_state');

    var SECONDS_IN_A_DAY = 24 * 60 * 60;
    var MILLISECONDS_IN_A_DAY = SECONDS_IN_A_DAY * 1000;

    self.get_today = function() {
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

    self.get_monday = function(today) {
        // Monday is day 1
        var offset = today.getDay() - 1;
        var monday = today - (offset * MILLISECONDS_IN_A_DAY);
        return new Date(monday);
    };

    self.get_week_commencing = function(today) {
        // today should be var today = new Date();
        var date = self.get_monday(today);
        return date.toISOString().substring(0,10);
    };

    self.error_state = function(im) {
        var _ = im.i18n;
        return new EndState(
            "end_state_error",
            _.gettext("Sorry! Something went wrong. Please redial and try again."),
            "initial_state"
        );
    };

    self.increment_and_fire = function(metric_key) {
        return function(){
            self.increment_and_fire_direct(metric_key);
        };
    };

    self.increment_and_fire_direct = function(metric_key) {
        var p = im.api_request('kv.incr', {
            key: metric_key,
            amount: 1
        });
        p.add_callback(function(result) {
            return im.metrics.fire(metric_key, result.value, 'max');
        });
        return p;
    };

    self.get_contact = function(im){
        var p = im.api_request('contacts.get_or_create', {
            delivery_class: 'ussd',
            addr: im.user_addr
        });
        return p;
    };

    self.make_navigation_choices = function(choices, prefix, parent) {
        var nav_choices = choices.map(function(choice) {
            var value = "";
            if (choice[0] == parent){
                value = parent;
            } else {
                value = prefix + "_" + choice[0];
            }
            var name = choice[1];
            return new Choice(value, name);
        });
        return nav_choices;
    };

    self.make_opinion_navigation_choices = function(choices, prefix, parent) {
        var nav_choices = choices.map(function(choice) {
            var value = prefix + "_" + choice[0];
            var name = choice[1];
            return new Choice(value, name);
        });
        return nav_choices;
    };

    self.make_question_choices = function(choices) {
        var nav_choices = choices.map(function(choice) {
            return new Choice(choice, choice);
        });
        return nav_choices;
    };

    self.make_question_state = function(prefix, question) {
         return function(state_name, im) {
            var choices = self.make_navigation_choices(
                question.choices,
                prefix,
                "main_menu"
            );

            return new ChoiceState(
                state_name,
                function(choice) {
                    return choice.value;
                },
                question.question,
                choices
            );
        };
    };

    //Dynamically builds the state
    self.make_mandl_question_state = function(state_name, prefix, next_state, question) {
        return function() {
            //Dynamically builds the choice list
            var choices = self.make_question_choices(question.choices);

            //Create the state, adding in the next state and the question itself
            return new ChoiceState(state_name, next_state, question.question, choices);
        };
    };

    self.make_mandl_thanks_state = function(state_name, quiz, quiz_name) {
         return function(state_name, im) {

            var _ = im.i18n;
            return new ChoiceState(
                state_name,
                function(choice) {
                    return choice.value;
                },
                _.gettext("Thanks! Carry on."),
                [
                    new Choice("continue", _.gettext("Main menu")),
                    new Choice("help_screen", _.gettext("Instructions to user USSD menu"))
                ],
                null,
                {
                    on_enter: function(){
                        var completed_question;
                        var completed_answer;
                        var p = new Promise();
                        for (var question_name in quiz.questions){
                            var question = quiz.questions[question_name].question;
                            var question_state_name = quiz_name + "_" + question_name;
                            completed_answer = im.get_user_answer(question_state_name);
                            p.add_callback(self.make_interaction_log("MANDL", question, completed_answer));
                        }
                        p.add_callback(self.mark_mandl_complete());
                        p.callback();
                        return p;
                    }
            });
        };
    };

    self.mark_mandl_complete = function(){
        return function(){
            var p = self.get_contact(im);
            p.add_callback(function(result) {
                // This callback updates extras when quiz finished
                if (result.contact["extras-ghr_mandl_inprog"] !== undefined){

                    var quiz_id = parseInt(result.contact["extras-ghr_mandl_inprog"]);
                    var completed_mandl = self.array_parse_ints(JSON.parse(result.contact["extras-ghr_questions"]));
                    completed_mandl.push(quiz_id);

                    // Airtime winner verification
                    var winner = "false";

                    if (self.is_winner()){
                        winner = self.get_week_commencing(self.get_today());
                    }

                    var fields = {
                        "ghr_mandl_inprog": "false",
                        "ghr_questions": JSON.stringify(completed_mandl),
                        "ghr_airtime_winner": winner
                    };
                    // Run the extras update
                    return im.api_request('contacts.update_extras', {
                        key: result.contact.key,
                        fields: fields
                    });
                }
            });
            return p;
        };
    };

    self.make_initial_question_state = function(state_name, prefix, question) {
        var choices = self.make_navigation_choices(question.choices, prefix, "main_menu");

        return new ChoiceState(state_name, function(choice) {
            return choice.value;
        }, question.question, choices, null,
            {
                on_enter: function() {
                    var p_log = self.increment_and_fire_direct("ghr_ussd_quiz_views");
                    return p_log;
                }
            }
        );
    };

    self.make_answer_state = function(prefix, answer) {
        return function(state_name, im) {
            var _ = im.i18n;
            return new ChoiceState(
                state_name,
                function(choice) {
                    return prefix + "_" + choice.value;
                },
                answer.response,
                [
                    new Choice(answer["next"], _.gettext("Next"))
                ]
            );
        };
    };

    self.add_state(new ChoiceState(
            "opinions_thank_you",
            "opinions",
            _.gettext("Thanks for sharing your opinion.\n"+
            "Press 1 to go back to the menu"),
            [
                new Choice("opinions", _.gettext("Continue"))
            ]
        )
    );

    self.get_opinion_result_text = function(im, opinion_counts) {
        var _ = im.i18n;
        var message = "";
        for (var i=0; i < opinion_counts.length; i++) {
            message += opinion_counts[i][1] + "% - "
                + _.gettext("Option '")
                + opinion_counts[i][0] + "'";
            if (i+1 < opinion_counts.length) {
                message += _.gettext("\n");
            }
        }
        message += "\n3. " + _.gettext('Main menu');
        return message;
    };

    self.add_creator("opinion_result",function(state_name, im) {
        var text =  self.get_opinion_result_text(im, im.user.opinion_counts);
        return new FreeText(
            state_name,
            function(content, done) {
                var next =  im.user.next_opinion_state;
                delete im.user.next_opinion_state;
                delete im.user.opinion_counts;
                done(next);
            },
            text
        );
    });

    self.add_creator("opinion_result_navigation",function(state_name,im) {
        var _ = im.i18n;
        return new FreeText(
            state_name,
            function(content) {
                if (content=="1") {
                    return "opinion_result";
                } else if (content=="3") {
                    return "main_menu";
                }
            },
            _.gettext("Press 1 to see the poll results and 3 to go to main menu."),
            function(content) {
                return (content=="1" || content=="3");
            },
            _.gettext("Error: Please press 1 to see the poll results and 3 to go to main menu.")
        );
    });

    self.increment_kv = function(im, key) {
        // Increment key value store
        var promise =  im.api_request('kv.incr', {
            key: key,
            amount: 1
        });
        return promise;
    };

    self.get_kv = function(im, key, i) {
        var promise = im.api_request('kv.get', {
            key: key
        });
        return promise;
    };

    //This will increment appropriate kv stores for opinions
    // 1. Will increment a total per question answered.
    // 2. Will increment a total for specific option for question answered.
    self.count_answers_of_opinions = function(im, opinion_name, opinion_value) {
        var promise = self.increment_kv(im, opinion_name);
        promise.add_callback(function() {
            return self.increment_kv(im, opinion_value);
        });
        return promise;
    };

    self.get_key_list = function(prefix, view, opinion_reference) {
        // Get a list of all keys
        var opinion_choices = view.choices;
        var opinion_choice_keys = [];
        for (var i=0; i < opinion_choices.length; i++) {
            var key = self.get_opinion_choice_kv_key(
                prefix,
                view,
                opinion_reference,
                opinion_choices[i][1]
            );
            opinion_choice_keys.push([key, opinion_choices[i][1]]);
        }
        return opinion_choice_keys;
    };

    //Needed to create a stack frame so that the callback used the correct item in the array
    self.add_opinion_kv_callback = function(im, promise, opinion_choice_keys, i) {
        promise.add_callback(function(count) {

            //Save the value of the opinion
            var total = im.user.opinion_total;
            var count = count.value || 0;

            var ratio = (total==0) ? 0 : Math.round(100*count/total);
            im.user.opinion_counts.push([opinion_choice_keys[i][1], ratio]);

            //If it's the last one, stop the chain.
            if (i+1 < opinion_choice_keys.length) {
                return self.get_kv(im, opinion_choice_keys[i + 1][0]);
            }
            else {
                return im.user.opinion_counts;
            }
        });
    };

    self.get_opinion_results = function(im, total_key, prefix, view, opinion_reference) {
        //Get key list for opinions
        var opinion_choice_keys = self.get_key_list(prefix,view,opinion_reference);

        //Get the total
        var promise = self.get_kv(im,total_key);

        //Assign the total and get the first choice value
        promise.add_callback(function(total_answers) {
            im.user.opinion_total = total_answers.value;
            im.user.opinion_counts = [];
            return self.get_kv(im, opinion_choice_keys[0][0]);
        });

        //Get every item
        for (var i=0; i < opinion_choice_keys.length; i++) {
            self.add_opinion_kv_callback(im, promise, opinion_choice_keys, i);
        }
        return promise;
    };

    self.make_view_state = function(prefix, view, view_name) {

        return function(state_name, im) {
            //Opinion navigation choices

            var choices = self.make_opinion_navigation_choices(
                view.choices,
                prefix,
                "opinions"
            );

            //Create choice state with provided name.
            return new ChoiceState(
                state_name,
                function(choice, done) {
                    var opinion_key = self.get_opinion_kv_key(prefix, view_name);
                    var opinion_choice_key = self.get_opinion_choice_kv_key(
                        prefix,
                        view,
                        view_name,
                        choice.label
                    );

                    //Count total questions answered
                    var promise =  self.count_answers_of_opinions(im, opinion_key, opinion_choice_key);
                    promise.add_callback(function() {
                        return self.get_opinion_results(
                            im, opinion_key,
                            prefix, view, view_name
                        );
                    });
                    promise.add_callback(function() {
                        im.user.next_opinion_state = choice.value;
                        done("opinion_result_navigation");
                    });

                    return promise;
                },
                view.opinions,
                choices,
                null,
                {
                    on_enter: function() {
                        var p_log = self.interaction_log(
                            "OPINIONS",
                            "viewed",
                            view.opinions
                        );
                        return p_log;
                    }
                });
        };
    };

    //Since we do not have unique identifier values
    //But we are recieving arrays of values
    //We can identify a user's choice based on the index in the array
    //But since we don't have this index to begin with,
    //We need to search the array of choices for the label
    self.get_opinion_choice_id_based_on_label = function(choices, label) {
        for (var i=0; i < choices.length; i++) {
            if (choices[i][1] === label) {
                return i+1;
            }
        }
        return null;
    };

    self.get_opinion_choice_kv_key = function(prefix, view, opinion_reference, label) {
        return [
            prefix,
            opinion_reference,
            self.get_opinion_choice_id_based_on_label(view.choices, label)
        ].join('_');
    };

    self.get_opinion_kv_key = function(prefix, opinion_reference) {
        return [
            prefix,
            opinion_reference,
            'total'
        ].join('_');
    };

    self.make_initial_view_state = function(im, state_name, prefix, view, start_opinion ) {
        //Build the navigation states
        var choices = self.make_navigation_choices(view.choices, prefix, null);

        //Create an actual state
        return new ChoiceState(state_name,
            function(choice,done) {
                var opinion_key = self.get_opinion_kv_key(prefix, start_opinion);

                var opinion_choice_key = self.get_opinion_choice_kv_key(
                    prefix,
                    view,
                    start_opinion,
                    choice.label
                );

                //Count total questions answered
                var promise =  self.count_answers_of_opinions(im, opinion_key, opinion_choice_key);
                promise.add_callback(function() {
                    return self.get_opinion_results(
                        im, opinion_key,
                        prefix, view, start_opinion
                    );
                });
                promise.add_callback(function() {
                    im.user.next_opinion_state = choice.value;
                    done("opinion_result_navigation");
                });
                return promise;
            },
            view.opinions,
            choices
        );
    };

    self.log_result = function(msg) {
        return function (result) {
            var p = im.log(msg + ', got result ' + JSON.stringify(result));
            p.add_callback(function() { return result; });
            return p;
        };
    };

    self.cache = function(cache_key, cache_lifetime, opts) {
        var lifetime = cache_lifetime || im.config.cache_lifetime;
        var func = opts.func;
        var func_arguments = opts.args;
        // attempt to fetch from the cache
        var p = im.log('Caching ' + cache_key);
        p.add_callback(function () {
            var kv_p = im.api_request('kv.get', {
                key: cache_key
            });
            kv_p.add_callback(function (result) {
                if(result.value) {
                    return JSON.parse(result.value);
                }
            });
            return kv_p;
        });
        p.add_callback(function (cached) {
            // if we have a result, check if it's still valid wrt lifetime
            if(cached) {
                var now = new Date();
                var timestamp = new Date(cached.timestamp);
                // subtracting dates gives milliseconds
                if(now - timestamp < (lifetime * 1000)) {
                    // still fresh, so return
                    var lp = im.log('Cache hit!');
                    lp.add_callback(function() {
                        return cached.result;
                    });
                    return lp;
                }
            }

            // doesn't exist or isn't fresh, do expensive function call
            var result_p = func.apply(self, func_arguments);
            result_p.add_callback(self.log_result('Cache miss'));
            result_p.add_callback(function (result) {
                // cache the results
                var cache_p = im.api_request('kv.set', {
                    key: cache_key,
                    value: JSON.stringify({
                        timestamp: new Date().toISOString(),
                        result: result
                    })
                });
                // when cached return the original result
                cache_p.add_callback(self.log_result('Cache set'));
                cache_p.add_callback(function (r) {
                    return result;
                });
                return cache_p;
            });
            return result_p;
        });
        return p;
    };

    self.crm_get = function(path) {
        var url = im.config.crm_api_root + path + "?format=json";
        var p = im.log('Starting crm_get: ' + path);
        p.add_callback(function() {
            return im.api_request("http.get", {
                url: url,
                headers: self.headers
            });
        });
        p.add_callback(function(result) {
            var json = self.check_reply(result, url, 'GET', null, false);
            return json;
        });
        p.add_callback(function(json) {
            var lp = im.log('Completed crm_get: ' + path);
            lp.add_callback(function() {
                return json;
            });
            return lp;
        });
        return p;
    };

    self.cached_crm_get = function (path) {
        return self.cache('cached_' + path, im.config.cache_lifetime, {
            func: self.crm_get,
            args: [path]
        });
    };

    self.crm_post = function(path, data) {
        var url = im.config.crm_api_root + path + "?format=json";
        data = self.url_encode(data);
        var p = im.log('Starting crm_post: ' + path);
        p.add_callback(function() {
            return im.api_request("http.post", {
                url: url,
                headers: self.post_headers,
                data: data
            });
        });
        p.add_callback(function(result) {
            var json = self.check_reply(result, url, 'POST', data, false);
            return json;
        });
        p.add_callback(function(json) {
            var lp = im.log('Completed crm_post: ' + path);
            lp.add_callback(function() {
                return json;
            });
            return lp;
        });
        return p;
    };

    self.make_interaction_log = function(feature, key, value) {
        return function() {
            self.interaction_log(feature, key, value);
        };
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

    self.survey_in_progress = function(contact) {
        if (typeof contact["extras-ghr_mandl_inprog"] !== 'undefined' &&
            JSON.parse(contact["extras-ghr_mandl_inprog"])) {
            return true;
        }
        return false;
    };

    self.is_winner = function() {
        if(im.config.testing) {
            return true;
        } else {
            if (im.config.airtime_reward_active && Math.floor((Math.random()*im.config.airtime_reward_chance)) === 0){
                return true;
            } else {
                return false;
            }
        }
    };


    self.make_mandl_or_mainmenu = function(state_name, contact,im){
        var completed_mandl = self.array_parse_ints(JSON.parse(contact["extras-ghr_questions"]));
        var quiz_id = false;
        var possible_mandl = self.array_parse_ints(im.config.mandl_quizzes);
        var incomplete_mandl = self.array_strip_duplicates(possible_mandl, completed_mandl);
        if (incomplete_mandl.length !== 0){
            quiz_id = incomplete_mandl[0];
        }
        if (!quiz_id) {
            // No survey left to do
            return self.make_main_menu(im);
        } else {
            // Mark contact with in progress quiz
            var fields = {
                "ghr_mandl_inprog": JSON.stringify(quiz_id)
            };
            // Run the extras update
            var p_e = im.api_request('contacts.update_extras', {
                key: contact.key,
                fields: fields
            });
            p_e.add_callback(function(){
                // Show the first state for the next quiz
                // Get first
                var quiz_name = "mandl_quiz_" + quiz_id + "_" + im.config.quizzes["mandl_quiz_" + quiz_id]["start"];
                return self.state_creators[quiz_name]();
            });
            return p_e;
        }
    };

    self.make_navigation_state = function(page, prefix, question, items, first, last, parent_hierarchy, parent_hierarchy_text, to_sub_nav) {

         return function(state_name, im) {
            var _ = im.i18n;
            var choices = items.map(function(item) {
                var value = prefix + "_" + self.clean_state_name(item);
                if (to_sub_nav) value+="_0";
                var name = item;
                return new Choice(value, name);
            });
            if (!first) choices.push(new Choice(prefix + "_" + (page-1), _.gettext("Back")));
            if (!last) choices.push(new Choice(prefix + "_" + (page+1), _.gettext("Next")));

            if (parent_hierarchy) {
                //If there hierarchy is more than 1 item
                if (parent_hierarchy instanceof Array) {

                    for (var i=0; i < parent_hierarchy.length; i++) {
                        choices.push(new Choice(parent_hierarchy[i],parent_hierarchy_text[i]));
                    }
                } else {
                    choices.push(new Choice(parent_hierarchy, parent_hierarchy_text));
                }
            }
            return new ChoiceState(state_name, function(choice) {
                return choice.value;
            }, question, choices);
        };
    };

    self.make_navigation_states = function(prefix, question, items, max_items, parent, parent_text) {
        // Generates the navigation paging states
        var total_pages = Math.ceil(items.length / max_items);
        var pages = [];
        var start = null;
        for (var i = 0; i < total_pages; i++){
            start = i*max_items;
            pages.push(items.slice(start, start+max_items));
        }
        var navigation_page_name = null;
        for (var p = 0; p < pages.length; p++){
            var first = (p===0) ? true : false;
            var last = (p==(pages.length-1)) ? true : false;
            // Give the state a name
            navigation_page_name = prefix + "_" + p;

            self.add_creator_unless_exists(
                navigation_page_name,
                self.make_navigation_state(
                    p,
                    prefix,
                    question,
                    pages[p],
                    first,
                    last,
                    parent,
                    parent_text,
                    true
                )
            );
        }
    };

    self.make_initial_navigation_state = function(state_name, prefix, question, items, last, parent, parent_text,im) {
        var _ = im.i18n;
        var choices = items.map(function(item) {
                var value = prefix + "_" + self.clean_state_name(item) + "_0";
                var name = item;
                return new Choice(value, name);
        });
        if (!last) choices.push(new Choice(prefix + "_1", _.gettext("Next")));
        if (parent) choices.push(new Choice(parent, parent_text));

        return new ChoiceState(state_name, function(choice) {
            return choice.value;
        }, question, choices, null,
            {
                on_enter: function() {
                    var p_log = self.increment_and_fire_direct("ghr_ussd_directory_views");
                    return p_log;
                }
            }
        );
    };

    self.make_booklet_state = function(end_state, content_array) {
        return function(state_name, im) {
            var next_page = function(page_number) {
                return content_array[page_number];
            };
            var _ = im.i18n;
            return new BookletState(
                state_name, {
                    next: end_state,
                    pages: (content_array.length-1),
                    page_text: next_page,
                    buttons: {
                        "1": -1, "2": +1, "3": "exit"
                    },
                    footer_text: _.gettext("\n1 for prev, 2 for next, 3 to end.")
                }
            );
        };
    };

    self.make_navigation_and_content_states = function(prefix, question, items, max_items, parent, parent_text) {

        // Generates the navigation paging states and related booklet_states
        var items_keys = Object.keys(items);
        var total_pages = Math.ceil(items_keys.length / max_items);
        var pages = [];
        var start = null;

        // Generates the pages
        for (var i = 0; i < total_pages; i++){
            start = i*max_items;
            pages.push(items_keys.slice(start, start+max_items));
        }

        // For each page
        var navigation_page_name = null;
        for (var p = 0; p < pages.length; p++){

            // Determine if first or last
            var first = (p===0) ? true : false;
            var last = (p==(pages.length-1)) ? true : false;

            // Give the state a name
            navigation_page_name = prefix + "_" + p;

            self.add_creator_unless_exists(
                navigation_page_name,
                self.make_navigation_state(
                    p,
                    prefix,
                    question,
                    pages[p],
                    first,
                    last,
                    parent,
                    parent_text,
                    false
                )
            );
        }
        for (var cat_name in items){
            var sub_cat = items[cat_name];
            var content = Object.keys(sub_cat).map(function (key) {
                return sub_cat[key];
            });
            var category_details_name = prefix + "_" + self.clean_state_name(cat_name);

            self.add_creator_unless_exists(category_details_name,
                                    self.make_booklet_state('end_state', content));
        }
    };

    self.validate_sector = function(im, sector) {
        return im.config.sectors.indexOf(sector.toLowerCase()) != -1;
    };

    self.unique_sector = function(im, sector) {
        return im.config.duplicates.indexOf(sector.toLowerCase()) == -1;
    };

    self.add_state(new ChoiceState(
            "help_screen",
            "main_menu",
            _.gettext("On the menu, press the number of the option you like to view.\n"+
            "Once you have chosen your option, you can navigate by choosing\n"+
            "1 for Prev, 2 for Next ,3 End session or 9 to go back to main menu."),
            [
                new Choice("main_menu", _.gettext("Continue"))
            ]
        )
    );

    self.check_directory = function(im){
        return im.config.directory_disable
    };

    self.make_main_menu = function(im){
        _ = im.i18n;
        var choices =  [
                 new Choice("articles", _.gettext("Articles")),
                 new Choice("opinions", _.gettext("Opinions")),
                 new Choice("wwsd", _.gettext("What would Shangazi do?")),
                 new Choice("quiz_start", _.gettext("Weekly quiz"))
             ]
        if (!self.check_directory(im)) {
            choices.push(new Choice("directory_start", _.gettext("Directory")))
        }
        return new ChoiceState(
            "main_menu",
            function(choice) {
                return choice.value;
            },
            "",
            choices,
            null,
            {
                on_enter: function() {
                    // Metric counting and logging
                    var wc = self.get_week_commencing(self.get_today());
                    var contact_key;

                    var p_c = self.get_contact(im);
                    p_c.add_callback(function(result){
                        contact_key = result.contact.key;
                        if (result.contact["extras-ghr_last_active_week"] !== undefined){
                            if (new Date(wc) > new Date(result.contact["extras-ghr_last_active_week"])){
                                var piafd = self.increment_and_fire_direct("ghr_ussd_total_users");
                                piafd.add_callback(function(result) {
                                    return true;
                                });
                                return piafd;
                            } else {
                                return false;
                            }
                        } else { // for contacts somehow missing attribute
                            return true;
                        }
                    });
                    p_c.add_callback(function(result){
                        if (result){
                            var fields = {
                                "ghr_last_active_week": wc
                            };
                            return im.api_request('contacts.update_extras', {
                                key: contact_key,
                                fields: fields
                            });
                        }
                    });
                    return p_c;
                }
            }
        );
    };

    self.make_main_menu_state = function() {
        return function(state_name, im) {
            return self.make_main_menu(im);
        };
    };


    self.array_parse_ints = function(target){
        return target.map(function(str) {
            return parseInt(str, 10);
        });
    };

    self.clean_state_name = function(target){
        return target.toLowerCase(          // 1) convert to lowercase
            ).replace(/-+/g, ''             // 2) remove dashes and pluses
            ).replace(/\s+/g, '_'           // 3) replace spaces with understore
            ).replace(/[^a-z0-9_]/g, ''     // 4) remove everything but alphanumeric characters and underscores
            );
    };

    self.array_strip_duplicates = function(in_array, from_array){
        return in_array.reduce(function(initial, each) {
            if(from_array.indexOf(each) == -1) {
                initial.push(each);
            }
            return initial;
        }, []);
    };

    self.add_creator('initial_state', function(state_name, im) {
        // Check if they've already registered
        var p = self.get_contact(im);

        p.add_callback(function(result) {
            // This callback creates extras if first time visitor - or just passes through
            im.set_user_lang('rw')
            if (result.contact["extras-ghr_reg_complete"] === undefined){
                // First visit - create extras
                var today = self.get_today(im);
                var week_commencing = self.get_week_commencing(today);
                var fields = {
                    "ghr_reg_complete": "false",
                    "ghr_reg_started": today.toISOString(),
                    "ghr_questions": JSON.stringify([]),
                    "ghr_gender": "",
                    "ghr_age": "",
                    "ghr_sector": "",
                    "ghr_terms_accepted": "false",
                    "ghr_last_active_week": week_commencing
                };
                // Run the extras update
                return im.api_request('contacts.update_extras', {
                    key: result.contact.key,
                    fields: fields
                });
            } else {
                // Not first so just pass previous callback result on
                return result;
            }
        });

        p.add_callback(function(result) {
            // This callback generates the state the user sees
            var _=im.i18n;
            if (result.success){
                if (result.contact["extras-ghr_reg_complete"] == "false"){
                    // Did not finish registration and session state not found
                    return new ChoiceState(
                    state_name,
                    "reg_gender",
                    _.gettext("Welcome to Ni Nyampinga:"),
                    [
                        new Choice("continue", _.gettext("Continue"))
                    ],
                        null,
                        {
                            on_enter: function() {
                                // Metric counting and logging
                                return self.increment_and_fire_direct("ghr_ussd_total_unique_users");
                            }
                        }
                    );
                } else {
                    // Registration complete so check for questions
                    // Check all question sets have been answered
                    return self.make_mandl_or_mainmenu(state_name, result.contact, im);
                }
            } else {
                // Something went wrong saving the extras
                return self.error_state(im);
            }
        });
        return p;  // return the promise
    });

    self.add_state(new EndState(
        "reg_noterms",
            _.gettext("Sorry but we can't proceed with your registration unless you accept the " +
        "Terms & Conditions. Please redial if you change your mind. Thanks!"),
        "initial_state"
    ));

    self.add_creator('reg_gender', function(state_name, im) {
        // Check if they've already registered
        var p = self.get_contact(im);

        p.add_callback(function(result) {
            // This callback updates extra to include terms accepted
            // Accepted terms
            var fields = {
                "ghr_terms_accepted": "true"
            };
            // Run the extras update
            return im.api_request('contacts.update_extras', {
                key: result.contact.key,
                fields: fields
            });
        });

        p.add_callback(function(result) {
            var _ = im.i18n;
            // This callback generates the state the user sees
            if (result.success){
                return new ChoiceState(
                    state_name,
                    "reg_age",
                    _.gettext("Please choose your gender:"),
                    [
                        new Choice("Male", _.gettext("Male")),
                        new Choice("Female", _.gettext("Female"))
                    ]
                );
            } else {
                return self.error_state(im);
            }
        });
        return p;
    });

    self.add_state(new ChoiceState(
            "reg_age",
            "reg_sector",
        _.gettext("Please choose your age:"),
            [
                new Choice("12 or under", _.gettext("12 or under")),
                new Choice("12-15", "12-15"),
                new Choice("16-18", "16-18"),
                new Choice("19-24", "19-24"),
                new Choice("25-35", "25-35"),
                new Choice("35+", "35+")
            ]
        )
    );

    self.add_state(new FreeText(
        "reg_sector",
        "reg_thanks",
        _.gettext("Which sector do you live in?\nPress 1 if you do not know")
    ));

    self.add_creator('reg_thanks', function(state_name, im) {
        var sector = im.get_user_answer('reg_sector');
        var gender = im.get_user_answer('reg_gender');
        var age = im.get_user_answer('reg_age');
        var district = im.get_user_answer("reg_district");
        var next_state;

        var _ = im.i18n;

        if (self.validate_sector(im, sector) || sector == "1") {
            // Get the user
            if (self.unique_sector(im, sector) || (!self.unique_sector(im, sector) && district) || sector == "1") {
                var p = self.get_contact(im);

                p.add_callback(function(result) {
                    // This callback updates extras when contact is found
                    var possible_mandl = self.array_parse_ints(im.config.mandl_quizzes);
                    next_state = 'mandl_quiz_' + possible_mandl[0]  + "_" + im.config.quizzes["mandl_quiz_" + possible_mandl[0]]["start"];
                    if (result.success){

                        var fields = {
                            "ghr_reg_complete": "true",
                            "ghr_gender": JSON.stringify(gender),
                            "ghr_age": JSON.stringify(age),
                            "ghr_sector": JSON.stringify(sector),
                            "ghr_district": JSON.stringify(district),
                            "ghr_mandl_inprog": JSON.stringify(possible_mandl[0])
                        };
                        // Run the extras update
                        return im.api_request('contacts.update_extras', {
                            key: result.contact.key,
                            fields: fields
                        });
                    } else {
                        // Error finding contact
                        return self.error_state(im);
                    }
                });
                p.add_callback(function(result) {
                    var _ = im.i18n;
                    if (result.success){
                        var girl = ["12 or under", "12-15", "16-18"];
                        return new ChoiceState(
                            state_name,
                            next_state,
                            _.gettext("Welcome Ni Nyampinga club member! We want to know you better. " +
                            "For each set of 4 questions you answer, you enter a lucky draw to " +
                            "win ") + im.config.airtime_reward_amount + _.gettext(" RwF weekly."),
                            [
                                new Choice("continue", _.gettext("Continue"))
                            ],
                            null,
                            {
                                on_enter: function() {
                                    var p_log = new Promise();
                                    p_log.add_callback(function(){return self.interaction_log("REGISTRATION", "gender", gender);});
                                    p_log.add_callback(function(){return self.interaction_log("REGISTRATION", "age", age);});
                                    if(sector!="1"){
                                        p_log.add_callback(function(){return self.interaction_log("REGISTRATION", "sector", sector);});
                                        if (district) {  // If not district this will not run
                                            p_log.add_callback(function(){return self.interaction_log("REGISTRATION", "district", district);});
                                        }
                                    }
                                    p_log.add_callback(self.increment_and_fire("ghr_ussd_total_registrations"));
                                    p_log.add_callback(function(){
                                        if (gender == "Female" && girl.indexOf(age)){
                                            return self.increment_and_fire("ghr_ussd_total_girl_registered_users");
                                        }
                                    });
                                    p_log.callback();
                                    return p_log;
                                }
                            });
                    } else {
                        // Error saving contact extras
                        return self.error_state(im);
                    }
                });
                return p;
            } else {
                return new FreeText(
                    "reg_district",
                    "reg_thanks",
                    _.gettext("What district are you in?")
                );
            }
        } else {
           return new FreeText(
                "reg_sector",
                "reg_thanks",
               _.gettext("Sorry, cannot find a match. Please try again.\nWhich sector do you live in?\nPress 1 if you do not know")

            );
        }
    });


    self.add_state(new FreeText(
        "reg_district",
        "reg_thanks",
        _.gettext("What district are you in?")
    ));

    self.add_creator('articles', function(state_name, im) {
        var p = self.crm_get("article/");
        var _=im.i18n;

        var footer =  [
         "\n2. "+ _.gettext("Next"),
         "\n1. "+ _.gettext("Prev") + ", 2. " + _.gettext("Next"),
         "\n1. "+ _.gettext("Prev") + ", 2. " + _.gettext("Next"),
         "\n1. "+ _.gettext("Prev") + ", 3. " + _.gettext("Main menu")
    ]

        p.add_callback(function(response) {
            var _=im.i18n;
            if (typeof(response.article) != "object"){
                return new ChoiceState(
                    state_name,
                    "main_menu",
                    _.gettext("Sorry there's no article this week, dial back soon!"),
                    [
                        new Choice("main_menu", _.gettext("Main menu"))
                    ]
                );
            } else {
                var next_page = function(page_number) {
                    return response.article[page_number] + footer[page_number];
                };
                return new BookletState(
                    state_name, {
                        next: 'main_menu',
                        pages: 4,
                        page_text: next_page,
                        buttons: {
                            "1": -1, "2": +1, "3": "exit"
                        },
                        footer_text: "",
                        handlers: {
                            on_enter: function() {
                                var p_log = new Promise();
                                p_log.add_callback(function(){return self.interaction_log("ARTICLES", "article", "viewed");});
                                p_log.add_callback(self.increment_and_fire("ghr_ussd_articles_views"));
                                p_log.callback();
                                return p_log;
                            }
                        }
                    }
                );
            }
        });
        return p;
    });

    self.add_state(new ChoiceState(
        "opinions",
        function(choice) {
            return choice.value;
        },
        _.gettext("Please choose an option:"),
        [
            new Choice("opinions_popular", _.gettext("Popular opinions from SMS")),
            new Choice("opinions_view", _.gettext("Leave your opinion")),
            new Choice("main_menu", _.gettext("Back"))
        ],
        null,
        {
            on_enter: function() {
                var p_log = self.increment_and_fire_direct("ghr_ussd_opinions_views");
                return p_log;
            }
        }
        )
    );


    self.add_creator('wwsd', function(state_name, im) {
        var _ = im.i18n;
        var footer =  [
         "\n2. "+ _.gettext("Next"),
         "\n1. "+ _.gettext("Prev") + ", 2. " + _.gettext("Next"),
         "\n1. "+ _.gettext("Prev") + ", 2. " + _.gettext("Next"),
         "\n1. "+ _.gettext("Prev") + ", 3. " + _.gettext("Main menu")
    ]
        var p = self.crm_get("shangazi/");
        p.add_callback(function(response) {
            var _ = im.i18n;
            if (response.shangazi === undefined){
                return new ChoiceState(
                    state_name,
                    "main_menu",
                    _.gettext("No new content this week"),
                    [
                        new Choice("main_menu", _.gettext("Main menu"))
                    ]
                );
            } else {
                var next_page = function(page_number) {
                    return response.shangazi[page_number] + footer[page_number];
                };
                return new BookletState(
                    state_name, {
                        next: 'main_menu',
                        pages: 4,
                        page_text: next_page,
                        buttons: {
                            "1": -1, "2": +1, "3": "exit"
                        },
                        footer_text: "",
                        handlers: {
                            on_enter: function() {
                                var p_log = new Promise();
                                p_log.add_callback(function(){return self.interaction_log("WWSD", "shangazi", "viewed");});
                                p_log.add_callback(self.increment_and_fire("ghr_ussd_ndabaga_views"));
                                p_log.callback();
                                return p_log;
                            }
                        }
                    }
                );
            }
            return response.shangazi[page_number];
        });
        return p;
    });

    self.add_creator('opinions_popular', function(state_name, im) {
        var _ = im.i18n;

        var next_page = function(page_number) {
            // We load the opinions in all in one go on_config_load
            if (page_number == 3){
               return _.gettext("Thank you_opinions") + footer[page_number]
            }
            else
            {
            return im.config.opinions["opinion_"+(page_number+1)] + footer[page_number];
            }

        };

        var footer =  [
             "\n2. " + _.gettext("Next"),
             "\n1. "+ _.gettext("Prev") + ", 2. " + _.gettext("Next"),
             "\n1. "+ _.gettext("Prev") + ", 2. " + _.gettext("Next"),
             "\n3. " + _.gettext("Main menu")
        ]
        var counter = 0;

        return new BookletState(
            state_name, {
                next: 'main_menu',
                pages: 4,
                page_text: next_page,
                buttons: {
                    "1": -1, "2": +1, "3": "exit"
                },
                footer_text: "",
                handlers: {
                    on_enter: function() {
                        var p_log = new Promise();
                        p_log.add_callback(function(){return self.interaction_log("OPINIONS", "popular", "viewed");});
                        p_log.add_callback(self.increment_and_fire("ghr_ussd_opinions_popular_views"));
                        p_log.callback();
                        return p_log;
                    }
                }
            }
        );
    });

    self.add_creator('opinions_view', function(state_name, im) {
        // Get the opinion
        var p_opinion_view = self.crm_get('opinions/view/');

        // Create the initial opinion viewing state.
        p_opinion_view.add_callback(function(result) {
            var collection = result.opinions;

            // Prefix to the first opinion
            var first_view_prefix = im.config.opinion_view[0];

            //The actual first opinion
            var first_view = im.config.opinion_view[1];
            var first_view_start_opinion = collection[first_view_prefix].start;

            //Construct state
            return self.make_initial_view_state(
                im,
                state_name,
                first_view_prefix,
                first_view,
                first_view_start_opinion
            );
        });
        return p_opinion_view;
    });

    self.add_creator('quiz_start', function(state_name, im) {
        // Get the user
        var p_weeklyquiz = self.crm_get('weeklyquiz/');
        p_weeklyquiz.add_callback(function(result) {
            // This callback checks extras when contact is found
            var quiz = result.quiz;
            if (!quiz) {
                return self.error_state(im);
            }
            var quiz_name = "weekly_quiz";
            return self.make_initial_question_state(state_name, quiz_name, quiz.quiz_details.questions[quiz['start']]);
        });
        return p_weeklyquiz;
    });

    self.add_creator('directory_start', function(state_name, im) {
        var _ = im.i18n;
        // Get the directory
        var p_dir = self.crm_get('directory/');
        p_dir.add_callback(function(result) {
            var directory = result.directory;
            var max_items = 3;
            var prefix = "directory";
            var question = _.gettext("Please select an option:");
            var items = Object.keys(directory);
            var last = (items.length <= max_items) ? true : false;
            return self.make_initial_navigation_state(state_name, prefix, question, items.slice(0,max_items), last, 'main_menu', _.gettext("Main menu"),im);
        });
        return p_dir;
    });

    self.add_state(new EndState(
        "end_state",
        _.gettext("Thank you and bye bye!"),
        "first_state"
    ));

    self.state_exists = function(state_name) {
        return self.state_creators.hasOwnProperty(state_name);
    };

    self.add_creator_unless_exists = function(state_name, state) {
        if(self.state_exists(state_name)) {
            return;
        }

        return self.add_creator(state_name, state);
    };

    self.build_mandl_quiz_states = function() {
        var p_mandl = self.cached_crm_get('mandl/');
        // load the quizzes
        p_mandl.add_callback(function(result) {
            var quizzes = result.quizzes;

            // Make the M&L quizzes available to other states too
            im.config.quizzes = quizzes;
            for (var quiz_name in quizzes){
                //Using name as index, get quiz
                var quiz = quizzes[quiz_name];

                // Create the quiz
                var previous_question = false;
                var previous_question_state_name = false;
                var item = 0;
                var num_questions = Object.keys(quiz.questions).length;

                //Iterate through questions
                for (var question_name in quiz.questions){

                    //Increment item?
                    item++;
                    var question = quiz.questions[question_name];

                    //Construct quiz name
                    var question_state_name = quiz_name + "_" + question_name;

                    // construct a function using make_mandl_question_state()
                    // to prevent getting a wrongly scoped 'question'

                    //If this is the 2nd item being processed
                    if (item > 1){

                        //Add the state creator for the previous state
                        //Since now we have the next state
                        self.add_creator_unless_exists(
                            previous_question_state_name,
                            self.make_mandl_question_state(
                                previous_question_state_name,
                                quiz_name,
                                question_state_name,
                                previous_question
                            )
                        );

                        //If this is the last question
                        if (num_questions == item){
                            var thanks_state_name = quiz_name + "_thanks";

                            // This is a buffer state that logs their responses to the question
                            self.add_creator_unless_exists(
                                thanks_state_name,
                                self.make_mandl_thanks_state(
                                    thanks_state_name,
                                    quiz,
                                    quiz_name
                                )
                            );

                            //Create the final quiz state, since there is no more iterations
                            self.add_creator_unless_exists(
                                question_state_name,
                                self.make_mandl_question_state(
                                    question_state_name,
                                    quiz_name,
                                    thanks_state_name,
                                    question
                                )
                            );
                        }
                    }
                    previous_question = question;
                    previous_question_state_name = question_state_name;
                }
            }
        });
        return p_mandl;
    };

    self.load_quizzes_config = function() {
        var p_mandl_all = self.cached_crm_get('mandl/all/');
        p_mandl_all.add_callback(function(result) {
            // Load all mandl quiz IDs
            im.config.mandl_quizzes = result.quizzes;
            return true;
        });
        return p_mandl_all;
    };

    self.load_opinions_config = function() {
        var p_opinion = self.cached_crm_get('opinions/sms/');
        p_opinion.add_callback(function(result){
            im.config.opinions = result.opinions;
            return true;
        });
        return p_opinion;
    };

    /*
    * The structure of what is returned by tastypie is:
    * {
    *   quiz: {
    *       quiz_details: {
    *           answers: {
    *               ...
    *           },
    *           questions: {
    *               q_x: {
    *                   question:"...",
    *                   choices: [...]
    *               },
    *               q_xx: {
    *                   question:"...",
    *                   choices: [...]
    *               }
    *           }
    *       },
    *       start: "q_x"
    *   }
    * }
    * */
    self.build_weekly_quiz_states = function() {
        //Get quizzes from cache
        var p_weeklyquiz = self.cached_crm_get('weeklyquiz/');
        p_weeklyquiz.add_callback(function(result) {

            // This callback checks extras when contact is found
            var quiz = result.quiz; //var quiz = result.quiz.quiz_details?

            if (!quiz) {
                return self.error_state(im);
            }
            var quiz_name = "weekly_quiz";
            var first_view_prefix = false;
            var first_view = false;

            // Create the quiz
            //For each question
            for (var question_name in quiz.quiz_details.questions){

                var question = quiz.quiz_details.questions[question_name];
                var question_state_name = quiz_name + "_" + question_name;

                // construct a function using make_question_state()
                // to prevent getting a wrongly scoped 'question'
                self.add_creator_unless_exists(question_state_name,
                    self.make_question_state(quiz_name, question));
            }

            // create the answer states
            for (var answer_name in quiz.quiz_details.answers){
                var answer = quiz.quiz_details.answers[answer_name];
                var answer_state_name = quiz_name + "_" + answer_name;

                self.add_creator_unless_exists(answer_state_name,
                    self.make_answer_state(quiz_name, answer));
            }
            // End of Build Weekly quiz
        });
        return p_weeklyquiz;
    };

    //Opinion view: is a set of opinions
    //Each opinion has a set of choices
    //Each opinion view: has a start opinion.
    self.build_opinion_states = function() {

        // Get the collection of opinion views from cache
        var p_opinion_view = self.cached_crm_get('opinions/view/');

        p_opinion_view.add_callback(function(result) {
            var collection = result.opinions;
            var first_view_prefix = false;
            var first_view = false;

            // For each opinion_view in the opinion view collection
            for (var opinion_view in collection){

                //If this is the first item, then save the first prefix
                if (!first_view_prefix) first_view_prefix = opinion_view;

                // Get opinions for relevant opinion view
                var opinions = collection[opinion_view];

                //For each opinion name in the views (badly named)
                for (var view_name in opinions.views){

                    //Get the actual objects
                    var view = opinions.views[view_name];

                    //Save the first opinion
                    if (!first_view) first_view = view;

                    //Create a name based on the view + opinion_name
                    var view_state_name = opinion_view + "_" + view_name;

                    // construct a function using make_view_state()
                    // to prevent getting a wrongly scoped 'view'
                    // opinion_view = the whole view
                    // view = an actual opinion with 'opinions' field and 'choices' field.
                    self.add_creator_unless_exists(
                        view_state_name,
                        self.make_view_state(opinion_view, view, view_name)
                    );
                }
            }
            im.config.opinion_view = [first_view_prefix, first_view];
            // End Build Opinion Viewing
        });
        return p_opinion_view;
    };

    self.build_directory_states = function() {
        // Build directory
        var p_directory = self.cached_crm_get('directory/');
        p_directory.add_callback(function(result) {
            var directory = result.directory;
            var max_items = 3;
            var prefix = "directory";
            var question = _.gettext("Please select an option:");
            var items = Object.keys(directory);
            self.make_navigation_states(
                prefix,
                question,
                items,
                max_items,
                'main_menu',
                _.gettext("Main menu")
            );
            for (var s=0; s<items.length;s++){
                var sub_question = _.gettext("Please select an organization:");
                var sub_items = directory[items[s]];
                var sub_prefix = prefix + "_" + self.clean_state_name(items[s]);
                self.make_navigation_and_content_states(
                    sub_prefix,
                    sub_question,
                    sub_items,
                    max_items,
                    ['directory_start','main_menu'],
                    [_.gettext("Back to categories"), _.gettext("Main menu")]
                );
            }
            // End Build directory
        });
        return p_directory;
    };

    self.build_sectors_array = function(){
        var p_sector = self.cached_crm_get('v1/sector/');

        var originals = [];
        var duplicates = [];
        p_sector.add_callback(function(result){
            var sectors = result.objects;
            for (var sector in sectors) {
                if (originals.indexOf(sectors[sector].name.toLowerCase()) == -1) {
                    originals.push(sectors[sector].name.toLowerCase());
                } else  {
                    duplicates.push(sectors[sector].name.toLowerCase());
                }
            }
            im.config.sectors = originals;
            im.config.duplicates = duplicates;
        });
        return p_sector;
    };

    self.on_config_read = function(event){
        // Run calls out to the APIs to load dynamic states
        var p = new Promise();
        p.add_callback(self.build_mandl_quiz_states);
        p.add_callback(self.load_quizzes_config);
        p.add_callback(self.load_opinions_config);
        p.add_callback(self.build_weekly_quiz_states);
        p.add_callback(self.build_opinion_states);
        p.add_callback(self.build_directory_states);
        p.add_callback(self.build_sectors_array);

        if(!self.state_exists('main_menu')) {
            self.add_creator('main_menu',
                self.make_main_menu_state());
        }

        p.callback();
        return p;
    };

    self.on_session_new = function(event) {
        return self.increment_and_fire_direct("ghr_ussd_total_sessions");
    };
}

// launch app
var states = new GoNikeGHR();
var im = new InteractionMachine(api, states);
im.attach();
