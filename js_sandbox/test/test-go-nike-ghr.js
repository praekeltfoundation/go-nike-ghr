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


describe("When using the USSD line", function() {

    describe("as an unregistered user", function() {
        // These are used to mock API reponses
        // EXAMPLE: Response from google maps API
        var fixtures = [
           // 'test/fixtures/example-geolocation.json'
        ];

        var tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    //user_store: "go_skeleton"
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
                response: "^Which sector do live in\\?$"
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
                content: "Valid sector",
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
                    "Which sector do live in\\?$"
                )
            });
            p.then(done, done);
        });

    });

});

