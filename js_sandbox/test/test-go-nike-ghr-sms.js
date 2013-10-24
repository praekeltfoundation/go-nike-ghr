var fs = require("fs");
var assert = require("assert");
var vumigo = require("vumigo_v01");
// CHANGE THIS to your-app-name
var app = require("../lib/go-nike-ghr-sms");

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

var swear_file = process.env.GHR_SWEAR_FILE || "fixtures/swear_words.json";
// for test fixtures where the data is all good
var test_fixtures_full = [
];

describe("When using the SMS line", function() {


    describe("as any user type", function() {
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
                    swear_words: JSON.parse(fs.readFileSync(swear_file)),
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/",
                    terms_url: "faketermsurl.com"
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });

        it("sending good text should say thanks", function (done) {
            var user = {};
            var p = tester.check_state({
                user: user,
                content: "This., -/ is #! an $ % ^ & * example ;: {} of a = -_ string with `~)() punctuation",
                next_state: "process_sms",
                response: "^Thanks for your SMS opinion!$",
                continue_session: false
            });
            p.then(function() {
                var updated_kv = tester.api.kv_store['ghr_sms_total_unique_users'];
                assert.equal(updated_kv, 1);
            }).then(done, done);
        });

        it("sending bad text should warn", function (done) {
            var user = {};
            var p = tester.check_state({
                user: user,
                content: "This., -/ is #! an $ % ^ & * example ;: {} of a = -_ poO with `~)() punctuation",
                next_state: "process_sms",
                response: "^Thanks for your SMS opinion! Please try to keep messages clean!$",
                continue_session: false
            });
            p.then(done, done);
        });

    });

    describe("as a spammer", function() {
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
                api.update_contact_extras(dummy_contact, {
                    "ghr_sms_opinion_last": "Pounding this message",
                    "ghr_sms_opinion_first_seen": "2013-05-01T18:27:01.209Z",
                    "ghr_sms_opinion_seen_count": '4',
                    "ghr_gender": "Male",
                    "ghr_age": "25-35",
                    "ghr_sector": "Test"
                });

                api.config_store.config = JSON.stringify({
                    testing: true,
                    testing_mock_today: [2013,4,2,8,10],
                    swear_words: JSON.parse(fs.readFileSync(swear_file)),
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/",
                    terms_url: "faketermsurl.com"
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });
    

        it("sending same text should warn", function (done) {
            var user = {};
            var p = tester.check_state({
                user: user,
                content: "Pounding this message",
                next_state: "process_sms",
                response: "^Thanks for your SMS opinion! Please try to keep messages clean!$",
                continue_session: false
            });
            p.then(done, done);
        });

    });

    describe("as a registered user", function() {
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
                api.update_contact_extras(dummy_contact, {
                    "ghr_reg_complete": "true",
                    "ghr_reg_started": "2013-05-24T08:27:01.209Z",
                    "ghr_gender": "Male",
                    "ghr_age": "25-35",
                    "ghr_sector": "Test"
                });

                api.config_store.config = JSON.stringify({
                    testing: true,
                    testing_mock_today: [2013,4,2,8,10],
                    swear_words: JSON.parse(fs.readFileSync(swear_file)),
                    crm_api_root: "http://ghr.preview.westerncapelabs.com/api/",
                    terms_url: "faketermsurl.com"
                });
                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });

        it("sending same text should thank and log metric", function (done) {
            var user = {};
            var p = tester.check_state({
                user: user,
                content: "Sending this message",
                next_state: "process_sms",
                response: "^Thanks for your SMS opinion!$",
                continue_session: false
            });
            p.then(function() {
                var updated_kv = tester.api.kv_store['ghr_sms_total_registered_users'];
                assert.equal(updated_kv, 1);
            }).then(function() {
                var updated_kv = tester.api.kv_store['ghr_sms_total_messages_received'];
                assert.equal(updated_kv, 1);
            }).then(function() {
                var updated_kv = tester.api.kv_store['ghr_sms_total_messages_sent'];
                assert.equal(updated_kv, 1);
            }).then(done, done);
        });
    });
});

