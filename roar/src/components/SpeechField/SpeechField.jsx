import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import './SpeechField.css';
import DFConvo from '../DFConvo/DFConvo'

class SpeechField extends Component {
    constructor(props) {
        super(props);
        this.state = {
            querying: false,
        };
    }

    changeInputSource = () => {
        this.setState({
            querying: true
        });
    }

    render() {
        return (
            <div>
                <div className="fullscreen-video-wrap">
                    <video
                        src="http://www.personal.psu.edu/jok5517/personalpaw/bg.mp4"
                        autoPlay="true"
                        loop="true"
                    />
                </div>
                <div>
                    <center>
                        <img
                            src="http://www.personal.psu.edu/jok5517/personalpaw/logo1.png"
                            alt="Personal Paw Logo"
                            style={{
                                width: "300px",
                                height: "250px",
                                marginTop: "8%",
                            }}
                        />
                    </center>
                </div>
                {
                    this.state.querying ?
                        <DFConvo /> :
                        <div className="initial-content">
                            <input
                                placeholder="Hey, ask me something..."
                                onClick={() => this.changeInputSource()}
                                type="text"
                                className="df-query"
                            />
                        </div>
                }
            </div>
        );
    }
}
export default SpeechField;