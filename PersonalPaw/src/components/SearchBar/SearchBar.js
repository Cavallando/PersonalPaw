import React, { Component } from 'react';
import { Toolbar } from 'react-native-material-ui';

import sendText from '../../assets/js/dfFunctions';

class SearchBar extends Component {
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
            <Toolbar
                leftElement="menu"
                centerElement="Searchable"
                searchable={{
                    autoFocus: true,
                    placeholder: 'Search',
                }}
                rightElement={{
                    menu: {
                        icon: "more-vert",
                        labels: ["item 1", "item 2"]
                    }
                }}
                onRightElementPress={(label) => { console.log(label) }}
            />

        );
    }
}

export default {SearchBar};