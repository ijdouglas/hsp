var welcome = {
    type: 'html-keyboard-response',
    stimulus: 'Welcome to the object similarity rating experiment'+
    "<p><b><i>Press any key to begin</i></b></p>"
};

var instructions = {
    type: "html-keyboard-response",
    stimulus: `
    <h1>Instructions</h1>
    <p align="justify">In the following experiment, you will see two pictures presented side by side in each trial. What you need to do is judge how similar the two pictures are, in terms of color, shape, and other visual features. Please give each pair a score between 1 and 7 (1 = very different, 7 = very similar). Please pay close attention to the pictures.</p>

    <p><b><i>Press any key to begin</i></b></p>`
};


function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * i)
        const temp = array[i]
        array[i] = array[j]
        array[j] = temp
    }
    return array;
}

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
    stimulus: "<p>That's all the image pairs. Thank you for your participation!</p><p>You can close this this page now, data will be automatically saved</p>"
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