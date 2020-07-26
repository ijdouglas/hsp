var welcome = {
    type: 'html-keyboard-response',
    stimulus: 'Welcome to the Human Simulation Paradigm for Verbs. Press any key to begin.'
};
var welcome2 = {
    type: 'html-keyboard-response',
    stimulus: 'Welcome to the human similarty judgement portion of the human simulation paradigm for verbs. Press any key to begin.'
};

var instructions = {
    type: "html-keyboard-response",
    stimulus: "<p>In this experiment you will be presented with silent videos " +
        "which contain a beep at the moment a verb was originally uttered.</p>" +
        "<p>Your task is to provide your best guess of what verb was most likely said during that beep.</p> <p><b>Please make sure your audio is on and turned up, so you can hear the beep.</b></p>" +
        "<p>Before you begin with the videos, you will hear a word and be asked to enter the heard word into a text box. After this initial test, the videos will begin.</p>" +
        "<p>The first set of videos will be training instances, where the " +
        "correct answer will be provided to you after your response.</p>" +
        "<p>The rest of the videos will be real trials with no correct answer provided.</p>" +
        "<p><b><i>Press any key to begin.</i></b></p>"
};

var instructions2 = {
    type: "html-keyboard-response",
    stimulus: `
    <h1>Instructions</h1>
    <p align="justify">You will be asked to watch some short videos of parents playing toys with their children. These videos are action verb naming instances selected from the toy-play interaction, which means that parent in the video named an action verb. The sound of each video is muted, and a beep is inserted at the onset of the verb that parent named. Your job is to carefully watch the video and then guess the intended verb at the moment of parent naming indicated by the beep.</p>

    <p align="justify">Please keep in mind that the verbs you are asked to guess are all <b>concrete action verbs</b> such as jump and clap. We are not asking you to guess abstract and generic verbs like "think", "see/look", "do", or "make". Please enter correctly spelled <b>English</b> verbs in <b>present tense only</b>.</p>

    <p align="justify">Each video will only be played once, so make sure you pay close attention to the entire video and only start typing the answer after the video. After the video, you have 20 seconds to enter your response. If you are unsure or do not know, please still try to provide your best guess within 20 seconds. If you did not enter a valid answer after 20 seconds, the next trial will start. If you <b>miss 5 consecutive trials</b>, the study will automatically stop.</p>

    <p align="justify">The study session will last 20 min, please make sure you have enough time to finish the study in one session. There will be no breaks in between.</p>

    <p>Let's do a sound check on the next page!</p>

    <p><b><i>Press any key to begin.</i></b></p>`
};



var instructions3 = {
    type: "html-keyboard-response",
    stimulus: `
    <h1>Instructions</h1>
    <p align="justify">You will be asked to look over word pairs and give a similarity judgement. These are concrete action verbs parents likely say to their children in a toy-play context. Your job is to carefully rate the similarity of the two words on a scale from 1 to 7 (1 = Not similar at all, 7 = Almost identical).</p>

    <p align="justify">The study session will last 20 or so min, please make sure you have enough time to finish the study in one session. There will be no breaks in between.</p>

    <p><b><i>Press any key to begin.</i></b></p>`
};
``

var end_training = {
    type: 'html-keyboard-response',
    stimulus: "<p>That's all the training examples. Now you're ready to begin labeling on your own.</p><p>Press any key to continue.</p>"
};

var ask_name = {
    type: 'survey-text',
    questions: [
        { prompt: "What is your name?" }
    ],
};

var form_survey_reminder = {
    type: 'html-keyboard-response',
    stimulus: "Please go back to the google form survey and complete PART 2"
};

var secret_word = {
    type: 'html-keyboard-response',
    stimulus: "Remember or write down the word \"<b>IU200</b>\". <p><b>You will be asked to enter this word in PART 2. In order to proceed to PART 2, you need to enter the correct word.</p></b>"
};


var end = {
    type: 'html-keyboard-response',
    stimulus: "That's all the videos. Thank you for participating! You can close this this page now, data will be automatically saved"
};
var end_words = {
    type: 'html-keyboard-response',
    stimulus: "That's all the word pairs. Thank you for participating! You can close this this page now, data will be automatically saved"
};

function baseName(str) {
    var base = new String(str).substring(str.lastIndexOf('/') + 1);
    if (base.lastIndexOf(".") != -1)
        base = base.substring(0, base.lastIndexOf("."));
    return base;
}


function validate_response(resp) {
    if (resp.length > 0) {
        return true;
    }

    return false;
}

jsPsych.plugins['hsp-free-response'] = (function () {

    var plugin = {};

    plugin.info = {
        name: 'hsp-free-response',
        trial_duration: {
            type: jsPsych.plugins.parameterType.INT,
            pretty_name: 'Trial duration',
            default: null,
            description: 'The maximum duration to wait for a response.'
        },
        parameters: {
            sources: {
                type: jsPsych.plugins.parameterType.VIDEO,
                pretty_name: 'Video',
                default: undefined,
                description: 'The video file to play.'
            },
            num_responses: {
                type: jsPsych.plugins.parameterType.INT,
                pretty_name: 'NumResponses',
                default: '',
                description: 'The number of responses fields available to subject.'
            },
            width: {
                type: jsPsych.plugins.parameterType.INT,
                pretty_name: 'Width',
                default: '',
                description: 'The width of the video in pixels.'
            },
            height: {
                type: jsPsych.plugins.parameterType.INT,
                pretty_name: 'Height',
                default: '',
                description: 'The height of the video display in pixels.'
            },
            autoplay: {
                type: jsPsych.plugins.parameterType.BOOL,
                pretty_name: 'Autoplay',
                default: true,
                description: 'If true, the video will begin playing as soon as it has loaded.'
            },
            controls: {
                type: jsPsych.plugins.parameterType.BOOL,
                pretty_name: 'Controls',
                default: false,
                description: 'If true, the subject will be able to pause the video or move the playback to any point in the video.'
            },
            questions: {
                type: jsPsych.plugins.parameterType.COMPLEX,
                array: true,
                pretty_name: 'Questions',
                default: undefined,
                nested: {
                    prompt: {
                        type: jsPsych.plugins.parameterType.STRING,
                        pretty_name: 'Prompt',
                        default: undefined,
                        description: 'Prompt for the subject to response'
                    },
                    placeholder: {
                        type: jsPsych.plugins.parameterType.STRING,
                        pretty_name: 'Value',
                        default: "",
                        description: 'Placeholder text in the textfield.'
                    },
                    rows: {
                        type: jsPsych.plugins.parameterType.INT,
                        pretty_name: 'Rows',
                        default: 1,
                        description: 'The number of rows for the response text box.'
                    },
                    columns: {
                        type: jsPsych.plugins.parameterType.INT,
                        pretty_name: 'Columns',
                        default: 40,
                        description: 'The number of columns for the response text box.'
                    },
                    required: {
                        type: jsPsych.plugins.parameterType.BOOL,
                        pretty_name: 'Required',
                        default: false,
                        description: 'Require a response'
                    },
                    name: {
                        type: jsPsych.plugins.parameterType.STRING,
                        pretty_name: 'Question Name',
                        default: '',
                        description: 'Controls the name of data values associated with this question'
                    }
                }
            },
            preamble: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'Preamble',
                default: null,
                description: 'HTML formatted string to display at the top of the page above all the questions.'
            },
            button_label: {
                type: jsPsych.plugins.parameterType.STRING,
                pretty_name: 'Button label',
                default: 'Continue',
                description: 'The text that appears on the button to finish the trial.'
            }
        }
    }

    plugin.trial = function (display_element, trial) {

        /*****************************************
            Setup for video playback element
        ******************************************/
        html = ''
        html += '<div>'
        html += '<video id="jspsych-video-keyboard-response-stimulus"';

        if (trial.width) {
            html += ' width="' + trial.width + '"';
        }
        if (trial.height) {
            html += ' height="' + trial.height + '"';
        }
        if (trial.autoplay) {
            html += " autoplay ";
        }
        if (trial.controls) {
            html += " controls ";
        }
        html += ">";

        var video_preload_blob = jsPsych.pluginAPI.getVideoBuffer(trial.sources[0]);
        if (!video_preload_blob) {
            for (var i = 0; i < trial.sources.length; i++) {
                var file_name = trial.sources[i];
                if (file_name.indexOf('?') > -1) {
                    file_name = file_name.substring(0, file_name.indexOf('?'));
                }
                var type = file_name.substr(file_name.lastIndexOf('.') + 1);
                type = type.toLowerCase();
                html += '<source src="' + file_name + '" type="video/' + type + '">';
            }
        }
        html += "</video>";
        html += "</div>";


        /*****************************************
            Setup for text response elements
        ******************************************/


        if (typeof trial.question.rows == 'undefined') {
            trial.question.rows = 1;
        }

        if (typeof trial.question.columns == 'undefined') {
            trial.question.columns = 40;
        }

        if (typeof trial.question.value == 'undefined') {
            // console.log("hello")
            trial.question.value = "";
        }

        // console.log(trial.question)

        if (trial.preamble !== null) {
            html += '<div id="jspsych-survey-text-preamble" class="jspsych-survey-text-preamble">' + trial.preamble + '</div>';
        }
        // start form
        html += '<form id="jspsych-survey-text-form">'

        q = trial.question

        html += '<div id="jspsych-survey-text-' + 1 + '" class="jspsych-survey-text-question" style="margin: 2em 0em;">';
        html += '<p class="jspsych-survey-text">' + q.prompt + '</p>';

        // console.log(trial.num_responses)

        for (var i = 0; i < trial.num_responses; i++) {
            var autofocus = i == 0 ? "autofocus" : "";
            var req = q.required ? "required" : "";
            html += '<input type="text" id="input-' + i + '"  name="#jspsych-survey-text-response-' + i + '" data-name="' + q.name + '" size="' + q.columns + '" ' + autofocus + ' ' + req + ' placeholder="' + q.placeholder + '"></input><br>';
        }


        // add submit button
        html += '<input type="submit" id="jspsych-survey-text-next" class="jspsych-btn jspsych-survey-text" value="' + trial.button_label + '"></input>';

        html += '</form>'

        display_element.innerHTML = html;

        // function end_trial() {

        //     // kill any remaining setTimeout handlers
        //     jsPsych.pluginAPI.clearAllTimeouts();

        //     // kill keyboard listeners
        //     jsPsych.pluginAPI.cancelAllKeyboardResponses();

        //     var endTime = performance.now();
        //     var response_time = endTime - startTime;

        //     var data = {
        //         video: file_name,
        //         words: []
        //     };

        //     var valid = true;

        //     for (var index = 0; index < trial.num_responses; index++) {
        //         var response = document.querySelector('#input-' + index).value;
        //         // if (!validate_response(response)) {
        //         //     valid = false;
        //         // }
        //         data.words.push(response)
        //     }

        //     var trial_data = {
        //         "rt": response_time,
        //         "response": JSON.stringify(data),
        //     };

        //     // clear the display
        //     display_element.innerHTML = '';

        //     // move on to the next trial
        //     jsPsych.finishTrial(trial_data);
        // };


        // // end trial if time limit is set
        // if (trial.trial_duration !== null) {
        //     jsPsych.pluginAPI.setTimeout(function () {
        //         end_trial();
        //         console.log(trial.trial_duration)
        //     }, trial.trial_duration);
        // }

        display_element.querySelector('#jspsych-survey-text-form').addEventListener('submit', function (e) {
            e.preventDefault();
            // measure response time
            var endTime = performance.now();
            var response_time = endTime - startTime;

            // create object to hold responses
            var data = {
                video: file_name,
                words: []
            };

            var valid = true;

            for (var index = 0; index < trial.num_responses; index++) {
                var response = document.querySelector('#input-' + index).value;
                // if (!validate_response(response)) {
                //     valid = false;
                // }
                data.words.push(response)
            }

            // save data
            var trialdata = {
                "rt": response_time,
                "response": JSON.stringify(data)
            };

            // console.log(trialdata)

            display_element.innerHTML = '';

            // console.log(valid)

            // next trial
            if (valid) {
                jsPsych.finishTrial(trialdata);
            } else {
                console.log("something is wrong")
                // alert("Your response is malformed, please check it")
                return;
            }
        });
        var startTime = performance.now();
    }
    return plugin;
})();

function saveData(name, data) {
    jsPsych.data.addProperties({ subject: ID });
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'write_data.php'); // 'write_data.php' is the path to the php file described above.
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ filename: name, filedata: data }));
}