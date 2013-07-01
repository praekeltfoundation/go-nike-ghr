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

function GoNikeGHR() {
    var self = this;
    // The first state to enter

    StateCreator.call(self, 'initial_state');

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

    self.add_creator('initial_state', function(state_name, im) {
        // Check if they've already registered
        var p = self.get_contact(im);

        p.add_callback(function(result) {
            // This callback creates extras if first time visitor - or just passes through
            if (result.contact["extras-ghr_reg_complete"] === undefined){
                // First visit - create extras
                var today = self.get_today(im);
                var fields = {
                    "ghr_reg_complete": "false",
                    "ghr_reg_started": today.toISOString(),
                    "ghr_questions": JSON.stringify([]),
                    "ghr_gender": "",
                    "ghr_age": "",
                    "ghr_sector": ""
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
            if (result.success){
                if (result.contact["extras-ghr_reg_complete"] == "false"){
                    // Did not finish registration and session state not found
                    return new ChoiceState(
                        state_name,
                        "reg_age",
                        "Please choose your gender:",
                        [
                            new Choice("Male", "Male"),
                            new Choice("Female", "Female")
                        ]
                    );
                } else {
                    // Registration complete so check for questions
                    // Check all question sets have been answered
                    // TODO: Make actual question completion status lookup
                    if (result.contact["extras-ghr_questions"] == '["1", "2", "3", "4"]') {
                        // All done so show menu
                        return new ChoiceState(
                            state_name,
                            function(choice) {
                                return choice.value;
                            },
                            "",
                            [
                                new Choice("articles", "Articles"),
                                new Choice("opinions", "Opinions"),
                                new Choice("wwnd", "What would Ndabaga do?"),
                                new Choice("quiz_start", "Weekly quiz"),
                                new Choice("directory_start", "Directory")
                            ]
                        );
                    } else {
                        // User still has unanswered M&L questions
                        // TODO
                        return new EndState(
                            "end_state",
                            "Will ask questions - Thank you and bye bye!",
                            "initial_state"
                        );
                    }
                }
            } else {
                // Something went wrong saving the extras
                return self.error_state();
            }
        });
        return p;  // return the promise
    });

    self.add_state(new ChoiceState(
            "reg_age",
            "reg_sector",
            "Please choose your age:",
            [
                new Choice("12 or under", "12 or under"),
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
        "Which sector do you live in?"
    ));

    self.add_creator('reg_thanks', function(state_name, im) {
        var sector = im.get_user_answer('reg_sector');
        if (sector=='Valid sector') {
            // Get the user
            var p = self.get_contact(im);

            p.add_callback(function(result) {
                // This callback updates extras when contact is found
                if (result.success){
                    var gender = im.get_user_answer('initial_state');
                    var age = im.get_user_answer('reg_age');
                    var fields = {
                        "ghr_reg_complete": "true",
                        "ghr_gender": gender,
                        "ghr_age": age,
                        "ghr_sector": sector
                    };
                    // Run the extras update
                    return im.api_request('contacts.update_extras', {
                        key: result.contact.key,
                        fields: fields
                    });
                } else {
                    // Error finding contact
                    return self.error_state();
                }
            });

            p.add_callback(function(result) {
                if (result.success){
                    return new ChoiceState(
                        state_name,
                        'end_state',
                        "Thank you for registering",
                        [
                            new Choice("continue", "Continue")
                        ]
                    );
                } else {
                    // Error saving contact extras
                    return self.error_state();
                }
            });
            return p;
        } else {
           return new FreeText(
                "reg_sector_reenter",
                "reg_thanks",
                "Sorry, cannot find a match. Please try again.\nWhich sector do you live in?"
            );
        }
    });

    self.get_article = function(){
        return "Lorem ipsum dolor sit amet, consectetur adipiscing elit.";
    };

    self.add_state(new BookletState(
        "articles",
        "end_state",
        3,
        self.get_article
    ));

    self.add_state(new EndState(
        "end_state",
        "Thank you and bye bye!",
        "first_state"
    ));
}

// launch app
var states = new GoNikeGHR();
var im = new InteractionMachine(api, states);
im.attach();

