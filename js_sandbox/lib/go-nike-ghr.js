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

    self.post_headers = {
        'Content-Type': ['application/x-www-form-urlencoded']
    };

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

    self.make_question_state = function(prefix, question) {
         return function(state_name, im) {
            var choices = question.choices.map(function(choice) {
                var name = "";
                if (choice[0] == "main_menu"){
                    name = "main_menu";
                } else {
                    name = prefix + "_" + choice[0];
                }
                var value = choice[1];
                return new Choice(name, value);
            });

            return new ChoiceState(state_name, function(choice) {
                return choice.value;
            }, question.question, choices, null,
                {
                    on_enter: function() {
                        var p_log = self.interaction_log("MANDL", "question_viewed", question.question);
                        return p_log;
                    }
                });
        };
    };

    self.make_initial_question_state = function(state_name, prefix, question) {
        var choices = question.choices.map(function(choice) {
            var name = "";
            if (choice[0] == "main_menu"){
                name = "main_menu";
            } else {
                name = prefix + "_" + choice[0];
            }
            var value = choice[1];
            return new Choice(name, value);
        });

        return new ChoiceState(state_name, function(choice) {
            return choice.value;
        }, question.question, choices);
    };

    self.make_answer_state = function(prefix, answer) {
        return function(state_name, im) {
            return new ChoiceState(
                state_name,
                function(choice) {
                    return prefix + "_" + choice.value;
                },
                answer.response,
                [
                    new Choice(answer["next"], "Next")
                ]
            );
        };
    },

    self.make_initial_mandl_question_state = function(state_name, prefix, question) {
            var choices = question.choices.map(function(choice) {
                var name = prefix + "_" + choice[0];
                var value = choice[1];
                return new Choice(name, value);
            });

            return new ChoiceState(state_name, function(choice) {
                return choice.value;
            }, question.question, choices, null,
                {
                    on_enter: function() {
                        var p_log = self.interaction_log("MANDL", "question_viewed", question.question);
                        return p_log;
                    }
                }
            );
    };

    self.make_view_state = function(prefix, view) {
         return function(state_name, im) {
            var choices = view.choices.map(function(choice) {
                var name = "";
                if (choice[0] == "opinions"){
                    name = "opinions";
                } else {
                    name = prefix + "_" + choice[0];
                }
                var value = choice[1];
                return new Choice(name, value);
            });

            return new ChoiceState(state_name, function(choice) {
                return choice.value;
            }, view.opinion, choices, null,
                {
                    on_enter: function() {
                        var p_log = self.interaction_log("OPINIONS", "viewed", view.opinion);
                        return p_log;
                    }
                });
        };
    };

    self.make_initial_view_state = function(state_name, prefix, view) {
        var choices = view.choices.map(function(choice) {
            var name = prefix + "_" + choice[0];
            var value = choice[1];
            return new Choice(name, value);
        });
        return new ChoiceState(state_name, function(choice) {
            return choice.value;
        }, view.opinion, choices);
    };

    self.crm_get = function(path) {
        var url = im.config.crm_api_root + path;
        var p = im.api_request("http.get", {
            url: url,
            headers: self.headers
        });
        p.add_callback(function(result) {
            var json = self.check_reply(result, url, 'GET', null, false);
            return json;
        });
        return p;
    };

    self.crm_post = function(path, data) {
        var url = im.config.crm_api_root + path;
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
        if (reply.success && reply.code == 200) {
            var json = JSON.parse(reply.body);
            return json;
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

    self.make_mandl_or_mainmenu = function(state_name, contact){
        var completed_mandl = self.array_parse_ints(JSON.parse(contact["extras-ghr_questions"]));
        var p2 = self.crm_get('mandl/all/');
        p2.add_callback(function(result) {
            // Strip out quizzes that we've done
            var incomplete_mandl = self.array_strip_duplicates(result.quizzes, completed_mandl);
            if (incomplete_mandl.length === 0){
                // There's no M&L quizzes incomplete
                return self.make_main_menu();
            } else {
                // Get's first incomplete quiz
                var quiz_id = incomplete_mandl[0];
                var quiz_name = "mandl_quiz_" + quiz_id;
                var quiz = im.config.quizzes[quiz_name];
                return self.make_initial_mandl_question_state(state_name, quiz_name, quiz.questions[quiz['start']]);
            }
        });
        return p2;
    };

    self.validate_sector = function(im, sector) {
        return im.config.sectors.indexOf(sector.toLowerCase()) != -1;
    };

    self.make_main_menu = function(){
        return new ChoiceState(
            "main_menu",
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
    };

    self.array_parse_ints = function(target){
        for (var i = 0; i < target.length; i++) {
            target[i] = parseInt(target[i],10);
        }
        return target;
    };

    self.array_strip_duplicates = function(in_array, from_array){
        for (var i = 0; i < in_array.length; i++) {
            if (from_array.indexOf(in_array[i]) != -1) {
                in_array.splice(i, 1);
                i--;
            }
        }
        return in_array;
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
                    return self.make_mandl_or_mainmenu(state_name, result.contact);
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
        var gender = im.get_user_answer('initial_state');
        var age = im.get_user_answer('reg_age');
        if (self.validate_sector(im, sector)) {
            // Get the user
            var p = self.get_contact(im);

            p.add_callback(function(result) {
                // This callback updates extras when contact is found
                if (result.success){
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
                        'mandl_builder',
                        "Thank you for registering",
                        [
                            new Choice("continue", "Continue")
                        ],
                        null,
                        {
                            on_enter: function() {
                                var p_log = self.interaction_log("REGISTRATION", "gender", gender);
                                p_log.add_callback(function() {
                                    var p_log2 = self.interaction_log("REGISTRATION", "age", age);
                                    p_log2.add_callback(function() {
                                        var p_log3 = self.interaction_log("REGISTRATION", "sector", sector);
                                        return p_log3;
                                    });
                                    return p_log2;
                                });
                                return p_log;
                            }
                        }
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

    self.add_creator('mandl_builder', function(state_name, im) {
        // Get the user
        var p = self.get_contact(im);

        p.add_callback(function(result) {
            // This callback checks extras when contact is found
            if (!result.success) {
                return self.error_state();
            }
            if (result.contact["extras-ghr_questions"] === undefined) {
                return self.error_state();
            }

            return self.make_mandl_or_mainmenu(state_name, result.contact);
        });
        return p;
    });

    self.add_creator('articles', function(state_name, im) {

        var next_page = function(page_number) {
            var p = self.crm_get("article/");
            p.add_callback(function(response) {
                return response.article[page_number];
            });
            return p;
        };

        return new BookletState(
            state_name, {
                next: 'end_state',
                pages: 4,
                page_text: next_page,
                buttons: {
                    "1": -1, "2": +1, "0": "exit"
                },
                footer_text: "\n1 for prev, 2 for next, 0 to end.",
                handlers: {
                    on_enter: function() {
                        var p_log = self.interaction_log("ARTICLES", "article", "viewed");
                        return p_log;
                    }
                }
            }
        );
    });

    self.add_state(new ChoiceState(
            "opinions",
            function(choice) {
                return choice.value;
            },
            "Please choose an option:",
            [
                new Choice("opinions_popular", "Popular opinions from SMS"),
                new Choice("opinions_view", "Leave your opinion"),
                new Choice("main_menu", "Back")
            ]
        )
    );


    self.add_creator('wwnd', function(state_name, im) {

        var next_page = function(page_number) {
            var p = self.crm_get("ndabaga/");
            p.add_callback(function(response) {
                return response.ndabaga[page_number];
            });
            return p;
        };

        return new BookletState(
            state_name, {
                next: 'end_state',
                pages: 4,
                page_text: next_page,
                buttons: {
                    "1": -1, "2": +1, "0": "exit"
                },
                footer_text: "\n1 for prev, 2 for next, 0 to end.",
                handlers: {
                    on_enter: function() {
                        var p_log = self.interaction_log("WWND", "ndabaga", "viewed");
                        return p_log;
                    }
                }
            }
        );
    });

    self.add_creator('opinions_popular', function(state_name, im) {

        var next_page = function(page_number) {
            // We load the opinions in all in one go on_config_load
            return im.config.opinions["opinion_"+(page_number+1)];
        };

        return new BookletState(
            state_name, {
                next: 'end_state',
                pages: 5,
                page_text: next_page,
                buttons: {
                    "1": -1, "2": +1, "0": "exit"
                },
                footer_text: "\n1 for prev, 2 for next, 0 to end.",
                handlers: {
                    on_enter: function() {
                        var p_log = self.interaction_log("OPINIONS", "popular", "viewed");
                        return p_log;
                    }
                }
            }
        );
    });

    self.add_creator('opinions_view', function(state_name, im) {
        var p_opinion_view = self.crm_get('opinion/view/');
        p_opinion_view.add_callback(function(result) {
            var collection = result.opinions;
            var first_view_prefix = im.config.opinion_view[0];
            var first_view = im.config.opinion_view[1];
            return self.make_initial_view_state(state_name, first_view_prefix, first_view);
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
                return self.error_state();
            }
            var quiz_name = "weekly_quiz";
            return self.make_initial_question_state(state_name, quiz_name, quiz.quiz_details.questions[quiz['start']]);
        });
        return p_weeklyquiz;
    });

    self.add_state(new EndState(
        "end_state",
        "Thank you and bye bye!",
        "first_state"
    ));

    self.on_config_read = function(event){
        // Run calls out to the APIs to load dynamic states

        var p_mandl = self.crm_get('mandl/');
        p_mandl.add_callback(function(result) {
            var quizzes = result.quizzes;
            // Make the M&L quizzes available to other states too
            im.config.quizzes = quizzes;
            for (var quiz_name in quizzes){
                var quiz = quizzes[quiz_name];
                // Create the quiz
                for (var question_name in quiz.questions){
                    var question = quiz.questions[question_name];
                    var question_state_name = quiz_name + "_" + question_name;
                    // do not recreate states that already exist.
                    if(self.state_creators.hasOwnProperty(question_state_name)) {
                        continue;
                    }
                    // construct a function using make_question_state()
                    // to prevent getting a wrongly scoped 'question'
                    self.add_creator(question_state_name,
                        self.make_question_state(quiz_name, question));
                }
            }
        });
        p_mandl.add_callback(function(){
            // Get 
            var p_opinion = self.crm_get('opinion/');
            p_opinion.add_callback(function(result){
                im.config.opinions = result.opinions;
                return true;
            });
            p_opinion.add_callback(function(){
                // Build Weekly quiz
                var p_weeklyquiz = self.crm_get('weeklyquiz/');
                p_weeklyquiz.add_callback(function(result) {
                    // This callback checks extras when contact is found
                    var quiz = result.quiz;
                    if (!quiz) {
                        return self.error_state();
                    }
                    var quiz_name = "weekly_quiz";
                    var first_view_prefix = false;
                    var first_view = false;
                    // Create the quiz
                    for (var question_name in quiz.questions){

                        var question = quiz.questions[question_name];
                        var question_state_name = quiz_name + "_" + question_name;

                        // do not recreate states that already exist.
                        if(self.state_creators.hasOwnProperty(question_state_name)) {
                            continue;
                        }

                        // construct a function using make_question_state()
                        // to prevent getting a wrongly scoped 'question'
                        self.add_creator(question_state_name,
                            self.make_question_state(quiz_name, question));
                    }

                    // create the answer states
                    for (var answer_name in quiz.quiz_details.answers){
                        var answer = quiz.quiz_details.answers[answer_name];
                        var answer_state_name = quiz_name + "_" + answer_name;

                        if(self.state_creators.hasOwnProperty(answer_state_name)) {
                            continue;
                        }

                        self.add_creator(answer_state_name,
                            self.make_answer_state(quiz_name, answer));
                    }
                    // End of Build Weekly quiz
                });
                p_weeklyquiz.add_callback(function(){
                    // Build Opinion Viewing
                    var p_opinion_view = self.crm_get('opinion/view/');
                    p_opinion_view.add_callback(function(result) {
                        var collection = result.opinions;
                        var first_view_prefix = false;
                        var first_view = false;
                        for (var opinion_view in collection){
                            if (!first_view_prefix) first_view_prefix = opinion_view;
                            var opinions = collection[opinion_view];
                            // Create the quiz
                            for (var view_name in opinions.views){
                                var view = opinions.views[view_name];
                                if (!first_view) first_view = view;
                                var view_state_name = opinion_view + "_" + view_name;
                                // do not recreate states that already exist.
                                if(self.state_creators.hasOwnProperty(view_state_name)) {
                                    continue;
                                }
                                // construct a function using make_view_state()
                                // to prevent getting a wrongly scoped 'view'
                                self.add_creator(view_state_name,
                                    self.make_view_state(opinion_view, view));
                            }
                        }
                        im.config.opinion_view = [first_view_prefix, first_view];
                        // End Build Opinion Viewing
                    });
                    return p_opinion_view;
                });
                return p_weeklyquiz;
            });
            return p_opinion;
        });
        return p_mandl;
    };
}

// launch app
var states = new GoNikeGHR();
var im = new InteractionMachine(api, states);
im.attach();
