import React, { Component } from 'react';
import sendText from '../../assets/js/dfFunctions.js';
import { Toolbar } from 'react-native-material-ui';

class SearchBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            queryText: "",
            querying: false,
            convo: []
        };
    }

    render() {
        return (
            <div>
                <Toolbar
                    leftElement="menu"
                    centerElement="Ask me something!"
                    searchable={{
                        autoFocus: true,
                        placeholder: 'Ask away..',
                        //onSubmitEditing: this.queryDF(e),
                        //onChangeText: this.updateQueryState(e)
                    }}
                    rightElement={{
                        menu: {
                            icon: "more-vert",
                            labels: ["item 1", "item 2"]
                        }
                    }}
                    onRightElementPress={(label) => { console.log(label) }}
                    ref={input => { this.dfinput = input; }}
                />
            </div>
        )
    }
}

export default SearchBar;