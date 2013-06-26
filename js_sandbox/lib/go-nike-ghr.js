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
    StateCreator.call(self, 'first_state');


    self.add_state(new FreeText(
        "first_state",
        "second_state",
        "Say something please..."
    ));

    self.add_creator('second_state', function(state_name, im) {
        return new ChoiceState(
            state_name,
            function(choice) {
                return (choice.value == 'yes' ? 'third_state' : 'end_state');
            },
            "Thank you! Do you what to know what you said?",
            [
                new Choice("yes", "Yes"),
                new Choice("no", "No")
            ]
            );
    });

    self.add_creator('third_state', function(state_name, im) {
        // go back to the first state answer
        var they_said = im.get_user_answer('first_state');
        return new ChoiceState(
            state_name,
            function(choice) {
                return (choice.value == 'yes' ? 'end_state_correct' : 'end_state_wrong');
            },
            "We think you said '" + they_said + "'. Correct?",
            [
                new Choice("yes", "Yes"),
                new Choice("no", "No")
            ]
            );
    });

    self.add_state(new EndState(
        "end_state_correct",
        "Aren't we clever? Thank you and bye bye!",
        "first_state"
    ));

    self.add_state(new EndState(
        "end_state_wrong",
        "Silly us! Thank you and bye bye!",
        "first_state"
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
