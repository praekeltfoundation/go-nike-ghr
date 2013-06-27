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
var InteractionMachine = vumigo.state_machine.InteractionMachine;
var StateCreator = vumigo.state_machine.StateCreator;

function GoNikeGHR() {
    var self = this;
    // The first state to enter

    StateCreator.call(self, 'initial_state');

    self.add_creator('initial_state', function(state_name, im) {
        return new ChoiceState(
            state_name,
            "reg_age",
            "Please choose your gender:",
            [
                new Choice("Male", "Male"),
                new Choice("Female", "Female")
            ]
            );
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
            return new ChoiceState(
                state_name,
                'end_state',
                "Thank you for registering",
                [
                    new Choice("continue", "Continue")
                ]
            );
        } else {
           return new FreeText(
                "reg_sector_reenter",
                "reg_thanks",
                "Sorry, cannot find a match. Please try again.\nWhich sector do you live in?"
            );
        }
    });

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

