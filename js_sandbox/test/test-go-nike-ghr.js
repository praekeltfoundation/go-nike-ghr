var fs = require("fs");
var assert = require("assert");
var vumigo = require("vumigo_v01");
// CHANGE THIS to your-app-name
var app = require("../lib/go-nike-ghr");

// This just checks that you hooked you InteractionMachine
// up to the api correctly and called im.attach();
describe("test_api", function() {
    it("should exist", function() {
        assert.ok(app.api);
    });
    it("should have an on_inbound_message method", function() {
        assert.ok(app.api.on_inbound_message);
    });
    it("should have an on_inbound_event method", function() {
        assert.ok(app.api.on_inbound_event);
    });
});

// for test fixtures where the data is all good
var test_fixtures_full = [
    'test/fixtures/mandl.json',
    'test/fixtures/article.json',
    'test/fixtures/mandl_all.json',
    'test/fixtures/ndabaga.json',
    'test/fixtures/opinions.json',
    'test/fixtures/opinions_view.json',
    'test/fixtures/userinteraction.json',
    'test/fixtures/userinteraction_age.json',
    'test/fixtures/userinteraction_sector.json',
    'test/fixtures/userinteraction_mandl.json',
    'test/fixtures/userinteraction_mandl_started.json',
    'test/fixtures/userinteraction_mandl_started2.json',
    'test/fixtures/userinteraction_mandl_2.json',
    'test/fixtures/userinteraction_mandl_3.json',
    'test/fixtures/userinteraction_mandl_4.json',
    'test/fixtures/userinteraction_articles.json',
    'test/fixtures/userinteraction_wwnd.json',
    'test/fixtures/userinteraction_opinions.json',
    'test/fixtures/userinteraction_opinions_popular.json',
    'test/fixtures/weekly_quiz.json',
    'test/fixtures/directory.json',
    'test/fixtures/hierarchy_sectors.json',
    'test/fixtures/userinteraction_sector_duplicates.json',
    'test/fixtures/userinteraction_sector_duplicates_district.json',
];

describe("When using the USSD line", function() {


    describe("as an unregistered user", function() {
        // These are used to mock API reponses
        // EXAMPLE: Response from google maps API
        var fixtures = test_fixtures_full;

        var tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);

                api.config_store.config = JSON.stringify({
                    testing: true,
                    testing_mock_today: [2013,5,1,8,10],
                    sectors: [],
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/",
                    terms_url: "faketermsurl.com",
                    airtime_reward_active: true,
                    airtime_reward_amount: 100,
                    airtime_reward_chance: 10,
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });

        // first test should always start 'null, null' because we haven't
        // started interacting yet

        it("first screen should ask us to accept T&Cs", function (done) {
            var p = tester.check_state({
                user: null,
                content: null,
                next_state: "initial_state",
                response: "^To proceed with registration, do you accept the Terms " +
                    "and Conditions of Ni Nyampinga - faketermsurl.com:[^]" +
                    "1. Yes[^]"+
                    "2. No$"
            });
            p.then(done, done);
        });

        it("declining T&C's should thanks and exit", function (done) {
            var user = {
                current_state: 'initial_state'
            };
            var p = tester.check_state({
                user: user,
                content: "2",
                next_state: "reg_noterms",
                response: "^Sorry but we can't proceed with your registration " +
                        "unless you accept the Terms & Conditions. Please redial " +
                        "if you change your mind. Thanks!$",
                continue_session: false
            });
            p.then(done, done);
        });


        it("accepting T&C's should ask us gender", function (done) {
            var user = {
                current_state: 'initial_state'
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "reg_gender",
                response: "^Please choose your gender:[^]" +
                    "1. Male[^]"+
                    "2. Female$"
            });
            p.then(done, done);
        });

        it("should ask age", function (done) {
            var user = {
                current_state: 'reg_gender',
                answers: {
                    initial_state: 'reg_gender'
                }
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "reg_age",
                response: (
                    "^Please choose your age:[^]" +
                    "1. 12 or under[^]" +
                    "2. 12\\-15[^]" +
                    "3. 16\\-18[^]" +
                    "4. 19\\-24[^]" +
                    "5. 25\\-35[^]" +
                    "6. 35\\+$"
                )
            });
            p.then(done, done);
        });

        it("should ask sector lived in", function (done) {
            var user = {
                current_state: 'reg_age',
                answers: {
                    initial_state: 'reg_gender',
                    reg_gender: 'Male'
                }
            };
            var p = tester.check_state({
                user: user,
                content: "4",
                next_state: "reg_sector",
                response: "^Which sector do you live in\\?$"
            });
            p.then(done, done);
        });

        it("entering valid sector should thank user", function (done) {
            var user = {
                current_state: 'reg_sector',
                answers: {
                    initial_state: 'reg_gender',
                    reg_gender: 'Male',
                    reg_age: '19-24'
                }
            };
            var p = tester.check_state({
                user: user,
                content: "Mareba",
                next_state: "reg_thanks",
                response: (
                    "^Welcome Ni Nyampinga club member! We want to know you better. " +
                    "For each set of 4 questions you answer, you enter a lucky draw to " +
                    "win 100 RwF weekly.[^]" +
                    "1. Continue$"
                )
            });
            p.then(done, done);
        });

        it("entering invalid sector should ask for reentry", function (done) {
            var user = {
                current_state: 'reg_sector',
                answers: {
                    initial_state: 'reg_gender',
                    reg_gender: 'Male',
                    reg_age: '19-24'
                }
            };
            var p = tester.check_state({
                user: user,
                content: "Invalid sector",
                next_state: "reg_sector",
                response: (
                    "^Sorry, cannot find a match. Please try again.\n" +
                    "Which sector do you live in\\?$"
                )
            });
            p.then(done, done);
        });

        it("entering a duplicate sector should ask for district", function (done) {
            var user = {
                current_state: 'reg_sector',
                answers: {
                    initial_state: 'reg_gender',
                    reg_gender: 'Male',
                    reg_age: '19-24'
                }
            };
            var p = tester.check_state({
                user: user,
                content: "Remera",
                next_state: "reg_district",
                response: (
                    "What district are you in?"
                )
            });
                p.then(done, done);
            });

        it("should register a user successfully with duplicate district", function(done){
            var user = {
                current_state: 'reg_thanks',
                answers: {
                    initial_state: 'reg_gender',
                    reg_gender: 'Male',
                    reg_age: '19-24',
                    reg_sector: 'Remera'
                }
            };

            var p = tester.check_state({
                user: user,
                content: "Gastibo",
                next_state: "reg_thanks",
                response: (
                    "^Welcome Ni Nyampinga club member! We want to know you better. " +
                    "For each set of 4 questions you answer, you enter a lucky draw to " +
                    "win 100 RwF weekly.[^]" +
                    "1. Continue$"
                )
            });
            p.then(done, done);
        });
    });

    describe("as a partially registered user - not completed any M&L questions", function() {
        // These are used to mock API reponses
        var fixtures = test_fixtures_full;

        var tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    testing: true,
                    testing_mock_today: [2013,5,1,8,10],
                    sectors: [],
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/",
                    airtime_reward_active: true,
                    airtime_reward_amount: 100,
                    airtime_reward_chance: 10,
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "ghr_reg_complete": "true",
                    "ghr_reg_started": "2013-05-24T08:27:01.209Z",
                    "ghr_questions": '[]',
                    "ghr_gender": "Male",
                    "ghr_age": "25-35",
                    "ghr_sector": "Test",
                    "ghr_mandl_inprog": '1',
                });
            },
            async: true
        });

        it("completed core registration details should ask M&L questions", function (done) {
            var user = {
                current_state: 'reg_thanks',
                answers: {
                    initial_state: 'Male',
                    reg_age: '19-24',
                    reg_sector: "Mareba"
                }
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "mandl_quiz_1_q_1",
                response: (
                    "^Is this fake question one\\?[^]" +
                    "1. Yes[^]" +
                    "2. No$"
                )
            });
            p.then(done, done);
        });

        it("answering first question should ask second M&L questions", function (done) {
            var user = {
                current_state: 'mandl_quiz_1_q_1',
                answers: {
                    reg_gender: 'Male',
                    reg_age: '19-24',
                    reg_sector: "Mareba"
                }
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "mandl_quiz_1_q_2",
                response: (
                    "^Is this fake question two?\\?[^]" +
                    "1. Of course[^]" +
                    "2. No way!$"
                )
            });
            p.then(done, done);
        });

        it("answering second question should show third question", function (done) {
            var user = {
                current_state: 'mandl_quiz_1_q_2',
                answers: {
                    reg_gender: 'Male',
                    reg_age: '19-24',
                    reg_sector: "Mareba",
                    mandl_quiz_1_q_1: 'Yes'
                }
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "mandl_quiz_1_q_3",
                response: (
                    "^Is this fake question three\\?[^]" +
                    "1. First[^]" +
                    "2. Second$"
                )
            });
            p.then(done, done);
        });

        it("answering third question should show thanks", function (done) {
            var user = {
                current_state: 'mandl_quiz_1_q_3',
                answers: {
                    reg_gender: 'Male',
                    reg_age: '19-24',
                    reg_sector: "Mareba",
                    mandl_quiz_1_q_1: 'Yes',
                    mandl_quiz_1_q_2: 'Of course'
                }
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "mandl_quiz_1_thanks",
                response: "^Thanks! Carry on.[^]" +
                    "1. Main menu$"
            });
            p.then(function() {
              var updated_contact = tester.api.contact_store['f953710a2472447591bd59e906dc2c26'];
              assert.equal(updated_contact['extras-ghr_airtime_winner'], "2013-05-27");
            }).then(done, done);
        });

        it("opting to continue should show main menu", function (done) {
            var user = {
                current_state: 'mandl_quiz_1_thanks',
                answers: {
                    reg_gender: 'Male',
                    reg_age: '19-24',
                    reg_sector: "Mareba",
                    mandl_quiz_1_q_1: 'Yes',
                    mandl_quiz_1_q_2: 'Of course',
                    mandl_quiz_1_q_3: 'First'
                }
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "main_menu",
                response: "^[^]" +
                    "1. Articles[^]" +
                    "2. Opinions[^]" +
                    "3. What would Ndabaga do\\?[^]" +
                    "4. Weekly quiz[^]" +
                    "5. Directory$"
            });
            p.then(done, done);
        });

    });


    describe("as an registered user - not completed all M&L questions", function() {
        // These are used to mock API reponses
        var fixtures = test_fixtures_full;

        var tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    testing: true,
                    testing_mock_today: [2013,5,1,8,10],
                    sectors: [],
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/",
                    airtime_reward_active: true,
                    airtime_reward_amount: 100,
                    airtime_reward_chance: 10,
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });


                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "ghr_reg_complete": "true",
                    "ghr_reg_started": "2013-05-24T08:27:01.209Z",
                    "ghr_questions": '["1"]',
                    "ghr_gender": "Male",
                    "ghr_age": "25-35",
                    "ghr_sector": "Test"
                });
            },
            async: true
        });

        // first test should always start 'null, null' because we haven't
        // started interacting yet
        it("first screen should ask us a question set we've not seen", function (done) {
            var p = tester.check_state({
                user: null,
                content: null,
                next_state: "mandl_quiz_2_q_1",
                response: "^Is this fake question three\\?[^]" +
                    "1. Yes[^]"+
                    "2. No$"
            });
            p.then(done, done);
        });
    });

    describe("as an registered user - completed all M&L questions", function() {
        // These are used to mock API reponses
        var fixtures = test_fixtures_full;

        var tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    testing: true,
                    testing_mock_today: [2013,5,1,8,10],
                    sectors: [],
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/",
                    airtime_reward_active: true,
                    airtime_reward_amount: 100,
                    airtime_reward_chance: 10,
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "ghr_reg_complete": "true",
                    "ghr_reg_started": "2013-05-24T08:27:01.209Z",
                    "ghr_questions": '["1", "2", "3", "4", "5"]',
                    "ghr_gender": "Male",
                    "ghr_age": "25-35",
                    "ghr_sector": "Test"
                });
            },
            async: true
        });

        // first test should always start 'null, null' because we haven't
        // started interacting yet
        it("first screen should show us menu", function (done) {
            var p = tester.check_state({
                user: null,
                content: null,
                next_state: "main_menu",
                response: "^[^]" +
                    "1. Articles[^]" +
                    "2. Opinions[^]" +
                    "3. What would Ndabaga do\\?[^]" +
                    "4. Weekly quiz[^]" +
                    "5. Directory$"
            });
            p.then(done, done);
        });

        it("selecting 1 from menu should show page one of article", function (done) {
            var user = {
                current_state: 'main_menu'
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "articles",
                response: (
                    "^Lorem ipsum dolor sit amet, consectetur adipiscing elit.[^]" +
                    "1 for prev, 2 for next, 0 to end.$"
                )
            });
            p.then(done, done);
        });

        it('show page two of article', function(done) {
            var p = tester.check_state({
                user: {
                    current_state: 'articles'
                },
                content: "2",
                next_state: 'articles',
                response: "^Proin a porta justo. Maecenas sem felis, sollicitudin vitae " +
                          "risus luctus, consectetur sollicitudin leo.[^]" +
                          "1 for prev, 2 for next, 0 to end.$"
            });
            p.then(done, done);
        });

        it('show page three of article', function(done) {
            var p = tester.check_state({
                user: {
                    pages: {
                        articles: 1
                    },
                    current_state: 'articles'
                },
                content: "2",
                next_state: 'articles',
                response: "^Donec tincidunt lobortis erat eget malesuada. Cras cursus " +
                          "accumsan eleifend. Morbi ullamcorper pretium sollicitudin.[^]" +
                          "1 for prev, 2 for next, 0 to end.$"
            });
            p.then(done, done);
        });

        it('show page four of article', function(done) {
            var p = tester.check_state({
                user: {
                    pages: {
                        articles: 2
                    },
                    current_state: 'articles'
                },
                content: "2",
                next_state: 'articles',
                response: "^Etiam tincidunt, sapien elementum pharetra dapibus, " +
                          "mi sem venenatis nulla, at interdum sapien augue eu elit.[^]" +
                          "1 for prev, 2 for next, 0 to end.$"
            });
            p.then(done, done);
        });

        it('should continue to page 1 after page 4', function(done) {
            var p = tester.check_state({
                user: {
                    pages: {
                        articles: 3
                    },
                    current_state: 'articles'
                },
                content: "2",
                next_state: 'articles',
                response: "^Lorem ipsum dolor sit amet, consectetur adipiscing elit.[^]" +
                          "1 for prev, 2 for next, 0 to end.$",
                continue_session: true
            });
            p.then(done, done);
        });

        it('should continue to end after article finish', function(done) {
            var p = tester.check_state({
                user: {
                    pages: {
                        articles: 2
                    },
                    current_state: 'articles'
                },
                content: "0",
                next_state: 'end_state',
                response: '^Thank you and bye bye!$',
                continue_session: false
            });
            p.then(done, done);
        });

        it("selecting 3 from menu should show page one of Ndabaga Opinions", function (done) {
            var user = {
                current_state: 'main_menu'
            };
            var p = tester.check_state({
                user: user,
                content: "3",
                next_state: "wwnd",
                response: (
                    "^Ndabaga ipsum dolor sit amet, consectetur adipiscing elit.[^]" +
                    "1 for prev, 2 for next, 0 to end.$"
                )
            });
            p.then(done, done);
        });

        it('show page two of Ndabaga Opinions', function(done) {
            var p = tester.check_state({
                user: {
                    current_state: 'wwnd'
                },
                content: "2",
                next_state: 'wwnd',
                response: "^Ndabaga a porta justo. Maecenas sem felis, sollicitudin vitae " +
                          "risus luctus, consectetur sollicitudin leo.[^]" +
                          "1 for prev, 2 for next, 0 to end.$"
            });
            p.then(done, done);
        });

        it('show page three of Ndabaga Opinions', function(done) {
            var p = tester.check_state({
                user: {
                    pages: {
                        wwnd: 1
                    },
                    current_state: 'wwnd'
                },
                content: "2",
                next_state: 'wwnd',
                response: "^Ndabaga tincidunt lobortis erat eget malesuada. Cras cursus " +
                          "accumsan eleifend. Morbi ullamcorper pretium sollicitudin.[^]" +
                          "1 for prev, 2 for next, 0 to end.$"
            });
            p.then(done, done);
        });

        it('show page four of Ndabaga Opinions', function(done) {
            var p = tester.check_state({
                user: {
                    pages: {
                        wwnd: 2
                    },
                    current_state: 'wwnd'
                },
                content: "2",
                next_state: 'wwnd',
                response: "^Ndabaga tincidunt, sapien elementum pharetra dapibus, " +
                          "mi sem venenatis nulla, at interdum sapien augue eu elit.[^]" +
                          "1 for prev, 2 for next, 0 to end.$"
            });
            p.then(done, done);
        });

        it('should continue to page 1 after page 4 of Ndabaga Opinions', function(done) {
            var p = tester.check_state({
                user: {
                    pages: {
                        wwnd: 3
                    },
                    current_state: 'wwnd'
                },
                content: "2",
                next_state: 'wwnd',
                response: "^Ndabaga ipsum dolor sit amet, consectetur adipiscing elit.[^]" +
                          "1 for prev, 2 for next, 0 to end.$",
                continue_session: true
            });
            p.then(done, done);
        });

        it('should continue to end after Ndabaga Opinions finish', function(done) {
            var p = tester.check_state({
                user: {
                    pages: {
                        wwnd: 2
                    },
                    current_state: 'wwnd'
                },
                content: "0",
                next_state: 'end_state',
                response: '^Thank you and bye bye!$',
                continue_session: false
            });
            p.then(done, done);
        });

        it("selecting 2 from menu should show Opinions submenu", function (done) {
            var user = {
                current_state: 'main_menu'
            };
            var p = tester.check_state({
                user: user,
                content: "2",
                next_state: "opinions",
                response: (
                    "^Please choose an option:[^]" +
                    "1. Popular opinions from SMS[^]" +
                    "2. Leave your opinion[^]" +
                    "3. Back$"
                )
            });
            p.then(done, done);
        });

        it("selecting 3 from Opinions submenu should return to the main menu", function (done) {
            var user = {
                current_state: 'opinions'
            };
            var p = tester.check_state({
                user: user,
                content: "3",
                next_state: "main_menu",
                response: (
                    "^[^]" +
                    "1. Articles[^]" +
                    "2. Opinions[^]" +
                    "3. What would Ndabaga do\\?[^]" +
                    "4. Weekly quiz[^]" +
                    "5. Directory$"
                )
            });
            p.then(done, done);
        });

        it("selecting 1 from Opinions submenu should display 1st of 5 opinions", function (done) {
            var user = {
                current_state: 'opinions'
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "opinions_popular",
                response: (
                    "^This is opinion one[^]" +
                    "1 for prev, 2 for next, 0 to end.$"
                )
            });
            p.then(done, done);
        });

        it("selecting 2 viewing 1st Opinion should display 2nd of 5 opinions", function (done) {
            var user = {
                current_state: 'opinions_popular'
            };
            var p = tester.check_state({
                user: user,
                content: "2",
                next_state: "opinions_popular",
                response: (
                    "^This is opinion two[^]" +
                    "1 for prev, 2 for next, 0 to end.$"
                )
            });
            p.then(done, done);
        });

        it("selecting 2 viewing 2nd Opinion should display 3rd of 5 opinions", function (done) {
            var user = {
                current_state: 'opinions_popular',
                pages: {
                    opinions_popular: 1
                }
            };
            var p = tester.check_state({
                user: user,
                content: "2",
                next_state: "opinions_popular",
                response: (
                    "^This is opinion three[^]" +
                    "1 for prev, 2 for next, 0 to end.$"
                )
            });
            p.then(done, done);
        });

        it("selecting 2 viewing 3rd Opinion should display 4th of 5 opinions", function (done) {
            var user = {
                current_state: 'opinions_popular',
                pages: {
                    opinions_popular: 2
                }
            };
            var p = tester.check_state({
                user: user,
                content: "2",
                next_state: "opinions_popular",
                response: (
                    "^This is opinion four[^]" +
                    "1 for prev, 2 for next, 0 to end.$"
                )
            });
            p.then(done, done);
        });

        it("selecting 2 viewing 4th Opinion should display 5th of 5 opinions", function (done) {
            var user = {
                current_state: 'opinions_popular',
                pages: {
                    opinions_popular: 3
                }
            };
            var p = tester.check_state({
                user: user,
                content: "2",
                next_state: "opinions_popular",
                response: (
                    "^This is opinion five[^]" +
                    "1 for prev, 2 for next, 0 to end.$"
                )
            });
            p.then(done, done);
        });

        it("selecting 0 viewing 5th Opinion should display thank you and end", function (done) {
            var user = {
                current_state: 'opinions_popular',
                pages: {
                    opinions_popular: 4
                }
            };
            var p = tester.check_state({
                user: user,
                content: "0",
                next_state: "end_state",
                response: (
                    "^Thank you and bye bye!$"
                ),
                continue_session: false
            });
            p.then(done, done);
        });

        it("selecting 2 from Opinions submenu should display an opinion to feedback on", function (done) {
            var user = {
                current_state: 'opinions'
            };
            var p = tester.check_state({
                user: user,
                content: "2",
                next_state: "opinions_view",
                response: (
                    "^I think something really clever[^]" +
                    "1. Yes, I agree[^]"+
                    "2. No way$"
                )
            });
            p.then(done, done);
        });

        it("selecting 1 in response to opinion displayed should display another opinion to feedback on", function (done) {
            var user = {
                current_state: 'opinions_view'
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "opinion_view_1_o_2",
                response: (
                    "^I think something really stupid[^]" +
                    "1. Yes, I agree[^]"+
                    "2. No way$"
                )
            });
            p.then(done, done);
        });

        it("selecting 2 in response to last opinion available should display Opinions sub menu", function (done) {
            var user = {
                current_state: 'opinion_view_1_o_2'
            };
            var p = tester.check_state({
                user: user,
                content: "2",
                next_state: "opinions",
                response: (
                    "^Please choose an option:[^]" +
                    "1. Popular opinions from SMS[^]" +
                    "2. Leave your opinion[^]" +
                    "3. Back$"
                )
            });
            p.then(done, done);
        });

        it("selecting 4 from menu should show first weekly quiz question", function (done) {
            var user = {
                current_state: 'main_menu'
            };
            var p = tester.check_state({
                user: user,
                content: "4",
                next_state: "quiz_start",
                response: (
                    "^Am I fake question 1\\?[^]" +
                    "1. Yes![^]" +
                    "2. No![^]" +
                    "3. Maybe!$"
                )
            });
            p.then(done, done);
        });

        it("selecting 1 from first weekly quiz question should give feedback", function (done) {
            var user = {
                current_state: 'quiz_start'
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "weekly_quiz_q_1_a_1",
                response: (
                    "^Yes -  Genius[^]" +
                    "1. Next$"
                )
            });
            p.then(done, done);
        });

        it("selecting 5 from menu should show the directory category listing", function (done) {
            var user = {
                current_state: 'main_menu'
            };
            var p = tester.check_state({
                user: user,
                content: "5",
                next_state: "directory_start",
                response: (
                    "^Please select an option:[^]" +
                    "1. category one[^]" +
                    "2. category two[^]" +
                    "3. category three[^]" +
                    "4. Next[^]" +
                    "5. Main menu$"
                )
            });
            p.then(done, done);
        });

        it("selecting 4 from directory should show the second page of directory category listing", function (done) {
            var user = {
                current_state: 'directory_start'
            };
            var p = tester.check_state({
                user: user,
                content: "4",
                next_state: "directory_1",
                response: (
                    "^Please select an option:[^]" +
                    "1. category four[^]" +
                    "2. category five[^]" +
                    "3. category six[^]" +
                    "4. Back[^]" +
                    "5. Next[^]" +
                    "6. Main menu$"
                )
            });
            p.then(done, done);
        });

        it("selecting 4 from directory page 2 should show the 1st page of directory category listing", function (done) {
            var user = {
                current_state: 'directory_1'
            };
            var p = tester.check_state({
                user: user,
                content: "4",
                next_state: "directory_0",
                response: (
                    "^Please select an option:[^]" +
                    "1. category one[^]" +
                    "2. category two[^]" +
                    "3. category three[^]" +
                    "4. Next[^]" +
                    "5. Main menu$"
                )
            });
            p.then(done, done);
        });

        it("selecting 5 from directory page 2 should show the last page of directory category listing", function (done) {
            var user = {
                current_state: 'directory_1'
            };
            var p = tester.check_state({
                user: user,
                content: "5",
                next_state: "directory_2",
                response: (
                    "^Please select an option:[^]" +
                    "1. category seven[^]" +
                    "2. category eight[^]" +
                    "3. Back[^]" +
                    "4. Main menu$"
                )
            });
            p.then(done, done);
        });

        it("selecting 1 from directory page 1 should show the first sub directory listing", function (done) {
            var user = {
                current_state: 'directory_start'
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "directory_category_one_0",
                response: (
                    "^Please select an organization:[^]" +
                    "1. sub category one[^]" +
                    "2. sub category two[^]" +
                    "3. Back to categories$"
                )
            });
            p.then(done, done);
        });

        it("selecting 2 from directory page 1 should show the second sub directory listing", function (done) {
            var user = {
                current_state: 'directory_start'
            };
            var p = tester.check_state({
                user: user,
                content: "2",
                next_state: "directory_category_two_0",
                response: (
                    "^Please select an organization:[^]" +
                    "1. sub category three[^]" +
                    "2. sub category four[^]" +
                    "3. Back to categories$"
                )
            });
            p.then(done, done);
        });

        it("selecting 1 from directory sub category one should show the first page of content", function (done) {
            var user = {
                current_state: 'directory_category_one_0'
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "directory_category_one_sub_category_one",
                response: (
                    "^first part of contact details[^]" +
                    "1 for prev, 2 for next, 0 to end.$"
                )
            });
            p.then(done, done);
        });

        it("selecting 2 from page 1 of content in directory sub category one should show the second page of content", function (done) {
            var user = {
                current_state: 'directory_category_one_sub_category_one'
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "directory_category_one_sub_category_one",
                response: (
                    "^second part of contact details[^]" +
                    "1 for prev, 2 for next, 0 to end.$"
                )
            });
            p.then(done, done);
        });

        it("selecting 2 from page 2 of content in directory sub category one should show the third page of content", function (done) {
            var user = {
                current_state: 'directory_category_one_sub_category_one',
                pages: {
                    directory_category_one_sub_category_one: 0
                }
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "directory_category_one_sub_category_one",
                response: (
                    "^second part of contact details[^]" +
                    "1 for prev, 2 for next, 0 to end.$"
                )
            });
            p.then(done, done);
        });

        it("selecting 0 from page 2 of content in directory sub category one show end_state", function (done) {
            var user = {
                current_state: 'directory_category_one_sub_category_one',
                pages: {
                    directory_category_one_sub_category_one: 0
                }
            };
            var p = tester.check_state({
                user: user,
                content: "0",
                next_state: "end_state",
                response: (
                    "^Thank you and bye bye!$"
                ),
                continue_session: false
            });
            p.then(done, done);
        });

    });

    describe("with no articles or Ndabaga in system", function() {
        // These are used to mock API reponses
        // EXAMPLE: Response from google maps API
        var fixtures = [
            'test/fixtures/article_none.json',
            'test/fixtures/ndabaga_none.json',
            'test/fixtures/mandl_all.json',
            'test/fixtures/mandl.json',
            'test/fixtures/opinions.json',
            'test/fixtures/opinions_view.json',
            'test/fixtures/weekly_quiz.json',
            'test/fixtures/directory.json',
            'test/fixtures/userinteraction_articles.json',
            'test/fixtures/userinteraction_wwnd.json',
            'test/fixtures/hierarchy_sectors.json',
        ];

        var tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "ghr_reg_complete": "true",
                    "ghr_reg_started": "2013-05-24T08:27:01.209Z",
                    "ghr_questions": '["1", "2", "3", "4", "5"]',
                    "ghr_gender": "Male",
                    "ghr_age": "25-35",
                    "ghr_sector": "Test"
                });

                api.config_store.config = JSON.stringify({
                    testing: true,
                    testing_mock_today: [2013,5,1,8,10],
                    sectors: [],
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/",
                    terms_url: "faketermsurl.com",
                    airtime_reward_active: true,
                    airtime_reward_amount: 100,
                    airtime_reward_chance: 10,
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });

        // first test should always start 'null, null' because we haven't
        // started interacting yet

        it("first screen should show us menu", function (done) {
            var p = tester.check_state({
                user: null,
                content: null,
                next_state: "main_menu",
                response: "^[^]" +
                    "1. Articles[^]" +
                    "2. Opinions[^]" +
                    "3. What would Ndabaga do\\?[^]" +
                    "4. Weekly quiz[^]" +
                    "5. Directory$"
            });
            p.then(done, done);
        });

        it("selecting 1 from menu should show no article available", function (done) {
            var user = {
                current_state: 'main_menu'
            };
            var p = tester.check_state({
                user: user,
                content: "1",
                next_state: "articles",
                response: (
                    "^Sorry there's no article this week, dial back soon![^]" +
                    "1. Main menu$"
                )
            });
            p.then(done, done);
        });

        it("selecting 3 from menu should show no Ndabaga available", function (done) {
            var user = {
                current_state: 'main_menu'
            };
            var p = tester.check_state({
                user: user,
                content: "3",
                next_state: "wwnd",
                response: (
                    "^No new content this week[^]" +
                    "1. Main menu$"
                )
            });
            p.then(done, done);
        });
    });
});
