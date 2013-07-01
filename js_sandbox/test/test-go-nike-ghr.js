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
                    testing: true,
                    testing_mock_today: [2013,5,1,8,10],
                    sectors: ["gashora", "juru", "kamabuye", "ntarama", "mareba", "mayange", "musenyi", "mwogo", "ngeruka", "nyamata", "nyarugenge", "rilima", "ruhuha", "rweru", "shyara", "gasange", "gastibo", "gitoki", "kabarore", "kageyo", "kiramuruzi", "kiziguro", "muhura", "murambi", "ngarama", "nyagihanga", "remera", "rugarama", "rwimbogo", "gahini", "kabare", "kabarondo", "mukarange", "murama", "murundi", "mwiri", "ndego", "nyamirama", "rukara", "ruramira", "rwinkwavu", "gahara", "gatore", "kigina", "kirehe", "mahama", "mpanga", "musaza", "mushikiri", "nasho", "nyamugari", "nyarubuye", "rusumo", "gashanda", "jarama", "karembo", "kazo", "kibungo", "mugesera", "murama", "mutenderi", "remera", "rukira", "rukumberi", "rurenge", "sake", "zaza", "gatunda", "kiyombe", "karama", "karangazi", "katabagemu", "matimba", "mimuli", "mukama", "musheli", "nyagatare", "rukomo", "rwempasha", "rwimiyaga", "tabagwe", "fumbwe", "gahengeri", "gishari", "karenge", "kigabiro", "muhazi", "munyaga", "munyiginya", "musha", "muyumbu", "mwulire", "nyakariro", "nzige", "rubona", "bumbogo", "gastata", "jali", "gikomero", "gisozi", "jabana", "kinyinya", "ndera", "nduba", "rusororo", "rutunga", "kacyiru", "kimihurura", "kimironko", "remera", "gahanga", "gatenga", "gikondo", "kagarama", "kanombe", "kicukiro", "kigarama", "masaka", "niboye", "nyarugunga", "gitega", "kanyinya", "kigali", "kimisagara", "mageragere", "muhima", "nyakabanda", "nyamirambo", "rwezamenyo", "bungwe", "butaro", "cyanika", "cyeru", "gahunga", "gatebe", "gitovu", "kagogo", "kinoni", "kinyababa", "kivuye", "nemba", "rugarama", "rugendabari", "ruhunde", "rusarabuge", "rwerere", "busengo", "coko", "cyabingo", "gakenke", "gashenyi", "mugunga", "jania", "kamubuga", "karambo", "kivuruga", "mataba", "minazi", "muhondo", "muyongwe", "muzo", "nemba", "ruli", "rusasa", "rushashi", "bukure", "bwisige", "byumba", "cyumba", "giti", "kaniga", "manyagiro", "miyoye", "kageyo", "mukarange", "muko", "mutete", "nyamiyaga", "nyankenke", "rubaya", "rukomo", "rushaki", "rutare", "ruvune", "rwamiko", "shangasha", "busogo", "cyuve", "gacaca", "gashaki", "gataraga", "kimonyi", "kinigi", "muhoza", "muko", "musanze", "nkosti", "nyange", "remera", "rwaza", "shingiro", "base", "burega", "bushoki", "buyoga", "cyinzuzi", "cyungo", "kinihira", "kisaro", "masoro", "mbogo", "murambi", "ngoma", "ntarabana", "rukozo", "rusiga", "shyorongi", "tumba", "gikonko", "gishubi", "kansi", "kibilizi", "kigembe", "mamba", "muganza", "mugombwa", "mukindo", "musha", "ndora", "nyanza", "save", "gishamvu", "karama", "kigoma", "kinazi", "maraba", "mbazi", "mukura", "ngoma", "ruhashya", "rusatira", "rwaniro", "simbi", "tumba", "gacurabwenge", "karama", "kayenzi", "kayumbu", "mugina", "musambira", "ngamba", "nyamiyaga", "nyarubaka", "rugalika", "rukoma", "runda", "cyeza", "kabacuzi", "kibangu", "kiyumba", "muhanga", "mushishiro", "nyabinoni", "nyamabuye", "nyarusange", "rongi", "rugendabari", "shyogwe", "buruhukiro", "cyanika", "gatare", "kaduha", "kamegeli", "kibirizi", "kibumbwe", "kitabi", "mbazi", "mugano", "musange", "musebeya", "mushubi", "nkomane", "gasaka", "tare", "uwinkingi", "busasamana", "busoro", "cyabakamyi", "kibirizi", "kigoma", "mukingo", "rwabicuma", "muyira", "ntyazo", "nyagisozi", "cyahinda", "busanze", "kibeho", "mata ", "munini", "kivu", "ngera", "ngoma", "nyabimata", "nyagisozi", "ruheru", "muganza", "ruramba", "rusenge", "bweramana", "byimana", "kabagari", "kinazi", "kinihira", "mbuye", "mwendo", "ntongwe", "ruhango", "bwishyura", "gishari", "gishyita", "gisovu", "gitesi", "kareba", "murambi", "mubuga", "mutuntu", "rubengera", "rugabano", "ruganda", "rwankuba", "twumba", "bwira", "gatumba", "hindiro", "kabaya", "kageyo", "kavumu", "matyazo", "muhanda", "muhororo", "ndaro", "ngororero", "nyange", "sovu", "bigogwe", "jenda", "jomba", "kabatwa", "karago", "kintobo", "mukamira", "muringa", "rambura", "rugera", "rurembo", "shyira", "bushekeri", "bushenge", "cyato", "gihombo", "kagano", "kanjogo", "karambi", "karengera", "kirimbi", "macuba", "mahembe", "nyabitekeri", "rangiro", "ruharambuga", "shangi", "bugeshi", "busasamana", "cyanzarwe", "gisenyi", "kanama", "kanzenze", "mudende", "nyakiliba", "nyamyumba", "nyundo", "rubavu", "rugerero", "bugarama", "butare", "bweyeye", "gikundamvura", "gashonga", "giheke", "gihundwe", "gitambi", "kamembe", "muganza", "mururu", "nkanka", "nkombo", "nkungu", "nyakabuye", "nyakarenzo", "nzahaha", "rwimbogo", "boneza", "gihango", "kigeyo", "kivumu", "manihira", "mukura", "murunda", "musasa", "mushonyi", "mushubati", "nyabirasi", "ruhango", "rusebeya"]
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

});

