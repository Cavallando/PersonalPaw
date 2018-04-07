import React, { Component } from 'react';
import { init, queryInputKeyDown } from '../../assets/js/layout.js';
import $ from 'jquery';
import SpeechRecognition from 'react-speech-recognition'
import PropTypes from 'prop-types';

const propTypes = {
    // Props injected by SpeechRecognition
    transcript: PropTypes.string,
    resetTranscript: PropTypes.func,
    browserSupportsSpeechRecognition: PropTypes.bool
}

class Speech extends Component {
    constructor(props) {
        super(props);
        this.state = {
            inputValue: '',
            resultDiv: null
        };
    }

    updateInputValue = (evt) => {
        this.setState({
            inputValue: evt.target.value
        });
    }
    componentDidMount() {
        init(this.resultDiv);
        this.setState({
            resultDiv: this.resultDiv
        })
    }

    render() {
        const { transcript, resetTranscript, browserSupportsSpeechRecognition } = this.props

        if (!browserSupportsSpeechRecognition) {
            return (
                <div class="content">
                    <div class="input-field">
                        <input placeholder="Hey, ask me something..." id="q" type="text" value={this.state.inputValue} onChange={evt => this.updateInputValue(evt)} />
                    </div>
                    <div id="result" ref={c => this.resultDiv = c}>
                    </div>
                </div>);
        }
        return (
            <div class="content">
                <div class="input-field">
                    <input placeholder="Hey, ask me something..." id="q" type="text" value={this.state.inputValue} onChange={evt => this.updateInputValue(evt)} />
                </div>
                <div id="result" ref={c => this.resultDiv = c}>
                </div>
            </div>
        );
    }
}
export default SpeechRecognition(Speech);