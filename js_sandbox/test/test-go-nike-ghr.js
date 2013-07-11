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

var sector_file = process.env.GHR_SECTOR_FILE || "fixtures/sectors.json";

describe("When using the USSD line", function() {


    describe("as an unregistered user", function() {
        // These are used to mock API reponses
        // EXAMPLE: Response from google maps API
        var fixtures = [
            'test/fixtures/mandl.json',
            'test/fixtures/article.json',
            'test/fixtures/mandl_all.json'
        ];

        var tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    testing: true,
                    testing_mock_today: [2013,5,1,8,10],
                    sectors: JSON.parse(fs.readFileSync(sector_file)),
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/"
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });

        // first test should always start 'null, null' because we haven't
        // started interacting yet
        it("first screen should ask us gender", function (done) {
            var p = tester.check_state({
                user: null,
                content: null,
                next_state: "initial_state",
                response: "^Please choose your gender:[^]" +
                    "1. Male[^]"+
                    "2. Female$"
            });
            p.then(done, done);
        });

        it("second screen should ask age", function (done) {
            var user = {
                current_state: 'initial_state'
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

        it("third screen should ask sector lived in", function (done) {
            var user = {
                current_state: 'reg_age',
                answers: {
                    initial_state: 'Male'
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

        it("forth screen with valid sector should thank user", function (done) {
            var user = {
                current_state: 'reg_sector',
                answers: {
                    initial_state: 'Male',
                    reg_age: '19-24'
                }
            };
            var p = tester.check_state({
                user: user,
                content: "Mareba",
                next_state: "reg_thanks",
                response: (
                    "^Thank you for registering[^]" +
                    "1. Continue$"
                )
            });
            p.then(done, done);
        });

        it("forth screen with invalid sector should ask for reentry", function (done) {
            var user = {
                current_state: 'reg_sector',
                answers: {
                    initial_state: 'Male',
                    reg_age: '19-24'
                }
            };
            var p = tester.check_state({
                user: user,
                content: "Invalid sector",
                next_state: "reg_sector_reenter",
                response: (
                    "^Sorry, cannot find a match. Please try again.\n" +
                    "Which sector do you live in\\?$"
                )
            });
            p.then(done, done);
        });

    });

    describe("as a partially registered user - not completed any M&L questions", function() {
        // These are used to mock API reponses
        var fixtures = [
            'test/fixtures/mandl.json',
            'test/fixtures/article.json',
            'test/fixtures/mandl_quiz.json',
            'test/fixtures/mandl_all.json'
        ];

        var tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    testing: true,
                    testing_mock_today: [2013,5,1,8,10],
                    sectors: JSON.parse(fs.readFileSync(sector_file)),
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/"
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });

                api._dummy_contacts = {
                    "f953710a2472447591bd59e906dc2c26": {
                        key: "f953710a2472447591bd59e906dc2c26",
                        surname: "Trotter",
                        user_account: "test-0-user",
                        bbm_pin: null,
                        msisdn: "1234567",
                        created_at: "2013-04-24 14:01:41.803693",
                        gtalk_id: null,
                        dob: null,
                        groups: null,
                        facebook_id: null,
                        twitter_handle: null,
                        email_address: null,
                        name: "Rodney",
                        "extras-ghr_reg_complete": "true",
                        "extras-ghr_reg_started": "2013-05-24T08:27:01.209Z",
                        "extras-ghr_questions": '[]',
                        "extras-ghr_gender": "Male",
                        "extras-ghr_age": "25-35",
                        "extras-ghr_sector": "Test"
                    }
                };

                api._handle_contacts_get_or_create = function(cmd, reply) {
                    var reply_contact = false;
                    for (var contact_key in api._dummy_contacts){
                        if (api._dummy_contacts[contact_key].msisdn == cmd.addr){
                            reply_contact = api._dummy_contacts[contact_key];
                        }
                    }
                    if (reply_contact){
                        reply({
                            success: true,
                            created: false,
                            contact: reply_contact
                        });
                    } else {
                        api._dummy_contacts['contact-key'] = api._new_contact;
                        api._dummy_contacts['contact-key'].msisdn = cmd.addr;
                        reply({
                            success: true,
                            created: true,
                            contact: api._new_contact
                        });
                    }
                };

                api._handle_contacts_update = function(cmd, reply) {
                    api._dummy_contacts[cmd.key] = cmd.fields;
                    reply({
                        success: true,
                        contact: api._dummy_contacts[cmd.key]
                    });
                };

                // TODO: This will break when contacts api gets changed to newer format
                api._handle_contacts_update_extras = function(cmd, reply) {
                    for (var k in cmd.fields) { api._dummy_contacts[cmd.key]['extras-'+k] = cmd.fields[k]; }
                    reply({
                        success: true,
                        contact: api._dummy_contacts[cmd.key]
                    });
                };
            },
            async: true
        });

        it("completed core registation details should ask M&L questions", function (done) {
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
                next_state: "mandl_builder",
                response: (
                    "^Is this fake question one\\?[^]" +
                    "1. Yes[^]" +
                    "2. No$"
                )
            });
            p.then(done, done);
        });

    });

    describe("as an registered user - not completed all M&L questions", function() {
        // These are used to mock API reponses
        var fixtures = [
            'test/fixtures/mandl.json',
            'test/fixtures/article.json',
            'test/fixtures/mandl_all.json'
        ];

        var tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    testing: true,
                    testing_mock_today: [2013,5,1,8,10],
                    sectors: JSON.parse(fs.readFileSync(sector_file)),
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/"
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });

                api._dummy_contacts = {
                    "f953710a2472447591bd59e906dc2c26": {
                        key: "f953710a2472447591bd59e906dc2c26",
                        surname: "Trotter",
                        user_account: "test-0-user",
                        bbm_pin: null,
                        msisdn: "1234567",
                        created_at: "2013-04-24 14:01:41.803693",
                        gtalk_id: null,
                        dob: null,
                        groups: null,
                        facebook_id: null,
                        twitter_handle: null,
                        email_address: null,
                        name: "Rodney",
                        "extras-ghr_reg_complete": "true",
                        "extras-ghr_reg_started": "2013-05-24T08:27:01.209Z",
                        "extras-ghr_questions": '["1"]',
                        "extras-ghr_gender": "Male",
                        "extras-ghr_age": "25-35",
                        "extras-ghr_sector": "Test"
                    }
                };

                api._handle_contacts_get_or_create = function(cmd, reply) {
                    var reply_contact = false;
                    for (var contact_key in api._dummy_contacts){
                        if (api._dummy_contacts[contact_key].msisdn == cmd.addr){
                            reply_contact = api._dummy_contacts[contact_key];
                        }
                    }
                    if (reply_contact){
                        reply({
                            success: true,
                            created: false,
                            contact: reply_contact
                        });
                    } else {
                        api._dummy_contacts['contact-key'] = api._new_contact;
                        api._dummy_contacts['contact-key'].msisdn = cmd.addr;
                        reply({
                            success: true,
                            created: true,
                            contact: api._new_contact
                        });
                    }
                };

                api._handle_contacts_update = function(cmd, reply) {
                    api._dummy_contacts[cmd.key] = cmd.fields;
                    reply({
                        success: true,
                        contact: api._dummy_contacts[cmd.key]
                    });
                };

                // TODO: This will break when contacts api gets changed to newer format
                api._handle_contacts_update_extras = function(cmd, reply) {
                    for (var k in cmd.fields) { api._dummy_contacts[cmd.key]['extras-'+k] = cmd.fields[k]; }
                    reply({
                        success: true,
                        contact: api._dummy_contacts[cmd.key]
                    });
                };
            },
            async: true
        });

        // first test should always start 'null, null' because we haven't
        // started interacting yet
        it("first screen should ask us a question set we've not seen", function (done) {
            var p = tester.check_state({
                user: null,
                content: null,
                next_state: "initial_state",
                response: "^Is this fake question three\\?[^]" +
                    "1. Yes[^]"+
                    "2. No$"
            });
            p.then(done, done);
        });
    });

    describe("as an registered user - completed all M&L questions", function() {
        // These are used to mock API reponses
        var fixtures = [
            'test/fixtures/mandl.json',
            'test/fixtures/article.json',
            'test/fixtures/mandl_all.json'
        ];

        var tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    testing: true,
                    testing_mock_today: [2013,5,1,8,10],
                    sectors: JSON.parse(fs.readFileSync(sector_file)),
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/"
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });

                api._dummy_contacts = {
                    "f953710a2472447591bd59e906dc2c26": {
                        key: "f953710a2472447591bd59e906dc2c26",
                        surname: "Trotter",
                        user_account: "test-0-user",
                        bbm_pin: null,
                        msisdn: "1234567",
                        created_at: "2013-04-24 14:01:41.803693",
                        gtalk_id: null,
                        dob: null,
                        groups: null,
                        facebook_id: null,
                        twitter_handle: null,
                        email_address: null,
                        name: "Rodney",
                        "extras-ghr_reg_complete": "true",
                        "extras-ghr_reg_started": "2013-05-24T08:27:01.209Z",
                        "extras-ghr_questions": '["1", "2", "3", "4", "5"]',
                        "extras-ghr_gender": "Male",
                        "extras-ghr_age": "25-35",
                        "extras-ghr_sector": "Test"
                    }
                };

                api._handle_contacts_get_or_create = function(cmd, reply) {
                    var reply_contact = false;
                    for (var contact_key in api._dummy_contacts){
                        if (api._dummy_contacts[contact_key].msisdn == cmd.addr){
                            reply_contact = api._dummy_contacts[contact_key];
                        }
                    }
                    if (reply_contact){
                        reply({
                            success: true,
                            created: false,
                            contact: reply_contact
                        });
                    } else {
                        api._dummy_contacts['contact-key'] = api._new_contact;
                        api._dummy_contacts['contact-key'].msisdn = cmd.addr;
                        reply({
                            success: true,
                            created: true,
                            contact: api._new_contact
                        });
                    }
                };

                api._handle_contacts_update = function(cmd, reply) {
                    api._dummy_contacts[cmd.key] = cmd.fields;
                    reply({
                        success: true,
                        contact: api._dummy_contacts[cmd.key]
                    });
                };

                // TODO: This will break when contacts api gets changed to newer format
                api._handle_contacts_update_extras = function(cmd, reply) {
                    for (var k in cmd.fields) { api._dummy_contacts[cmd.key]['extras-'+k] = cmd.fields[k]; }
                    reply({
                        success: true,
                        contact: api._dummy_contacts[cmd.key]
                    });
                };
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

    });
});

