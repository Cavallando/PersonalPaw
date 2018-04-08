import React from 'react';

import './DFConvo.css'
import sendText from '../../assets/js/demoFunctions.js';

class DFConvo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            queryText: "",
            querying: false,
            convo: []
        };
    }

    componentDidMount() {
        this.dfinput.focus();
    }

    updateQueryState(e) {
        this.setState({ queryText: e.target.value });
    }

    queryDF(e) {
        e.preventDefault();
        let tempQueryText = null;

        if (this.state.queryText) {
            tempQueryText = this.state.queryText;
            const date = new Date();

            this.setState({
                convo: [
                    <QueryNode
                        query={this.state.queryText}
                        key={date.getTime()}
                    />,
                    ...this.state.convo
                ],
                querying: true,
                queryText: "",
            });

            sendText(tempQueryText)
                .then((res) => {
                    let result = null;

                    try {
                        result = res.result.fulfillment.speech;
                    } catch (error) {
                        result = null;
                    }

                    if (result) {
                        this.setState({
                            convo: [
                                <ResponseNode
                                    response={result}
                                    key={res.id}
                                />,
                                ...this.state.convo
                            ],
                        });
                    }
                });
        }
    }

    render() {
        return (
            <div className="content">
                <form onSubmit={e => this.queryDF(e)}>
                    <input
                        placeholder="Hey, ask me something..."
                        type="text"
                        className="df-query"
                        ref={input => { this.dfinput = input; }}
                        value={this.state.queryText}
                        onChange={e => this.updateQueryState(e)}
                    />
                </form>
                {this.state.querying &&
                        <ul className="">
                            {this.state.convo}
                        </ul>
                }
            </div>
        );
    }
}

const QueryNode = ({ query }) => (
    <li className="clearfix right-align right card-panel blue-grey hoverable">
        {query}
    </li>
);

const ResponseNode = ({ response }) => {
    let data = null;

    try {
        data = JSON.parse(response);
        // console.log(data)

        let menu = null;
        if (data.food_items) {
            menu = data.food_items.map(item => (
                <li key={Math.random().toString(36).substr(2, 18)}>{item}</li>
            ))
        }

        return (
            <li className="clearfix left-align left card-panel blue-grey-text hoverable">
                {data.text}
                {data.image &&
                    <div>
                        <br/>
                        <a href={data.link}>
                            <img src={data.image} alt={data.text} />
                        </a>
                    </div>
                }
                {data.food_items &&
                    <div>
                        <ul>
                            {menu}
                        </ul>
                        The full menu can be found at
                        <a href="http://menu.hfs.psu.edu"> http://menu.hft.psu.edu</a>
                    </div>
                }
            </li>
        );
    } catch (error) {
        data = response
        return (
            <li className="clearfix left-align left card-panel blue-grey-text hoverable">
                {data}
            </li>
        );
    }
};

export default DFConvo;