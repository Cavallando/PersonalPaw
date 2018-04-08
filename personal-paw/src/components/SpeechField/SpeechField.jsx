import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import './SpeechField.css';
import 'animate.css';
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
                        <div className="header"><p style={{marginRight: "10px"}} className=" title mega animated fadeInLeftBig">Personal</p> <p className="title mega animated fadeInRightBig">Paw</p></div>
                    </center>
                </div>
                {
                    this.state.querying ?
                        <div className="convo"><DFConvo /></div> :
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