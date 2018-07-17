import React, { Component } from "react";
import Header from "./components/Header";
import SearchButton from "./components/SearchButton";
import { SafeAreaView, View, Text, StyleSheet } from "react-native";

//imported modules
import SearchBar from 'react-native-searchbar';
import Voice from 'react-native-voice';

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      searching: false,
      recognized: '',
      pitch: '',
      error: '',
      end: '',
      started: '',
      results: [],
      partialResults: [],
    };

    Voice.onSpeechStart = this.onSpeechStart.bind(this);
    Voice.onSpeechRecognized = this.onSpeechRecognized.bind(this);
    Voice.onSpeechEnd = this.onSpeechEnd.bind(this);
    Voice.onSpeechError = this.onSpeechError.bind(this);
    Voice.onSpeechResults = this.onSpeechResults.bind(this);
    Voice.onSpeechPartialResults = this.onSpeechPartialResults.bind(this);
    Voice.onSpeechVolumeChanged = this.onSpeechVolumeChanged.bind(this);
  }


  componentWillUnmount() {
    Voice.destroy().then(Voice.removeAllListeners);
  }

  onSpeechStart(e) {
    this.setState({
      started: '√',
    });
  }

  onSpeechRecognized(e) {
    this.setState({
      recognized: '√',
    });
  }

  onSpeechEnd(e) {
    this.setState({
      end: '√',
    });
  }

  onSpeechError(e) {
    this.setState({
      error: JSON.stringify(e.error),
    });
  }

  onSpeechResults(e) {
    this.setState({
      results: e.value,
    });
    console.log(e.value);
    Voice.stop();
  }

  onSpeechPartialResults(e) {
    this.setState({
      partialResults: e.value,
    });
  }

  onSpeechVolumeChanged(e) {
    this.setState({
      pitch: e.value,
    });
  }

  silenceCheck(e) {
    e._stopRecognizing();
  }
  silentVoiceStop(e) {
    clearTimeout(window.silenceSetTimeout);
    window.silenceSetTimeout = setTimeout(() => { e.silenceCheck(e) }, 2000);
  }

  async _startRecognizing(e) {
    this.setState({
      recognized: '',
      pitch: '',
      error: '',
      started: '',
      results: [],
      partialResults: [],
      end: ''
    });
    try {
      await Voice.start('en-US');
    } catch (e) {
      console.error(e);
    }
  }

  async _stopRecognizing(e) {
    try {
      await Voice.stop();
    } catch (e) {
      console.error(e);
    }
  }

  async _cancelRecognizing(e) {
    try {
      await Voice.cancel();
    } catch (e) {
      console.error(e);
    }
  }

  async _destroyRecognizer(e) {
    try {
      await Voice.destroy();
    } catch (e) {
      console.error(e);
    }
    this.setState({
      recognized: '',
      pitch: '',
      error: '',
      started: '',
      results: [],
      partialResults: [],
      end: ''
    });
  }

  _onSearchButtonClick(e) {
    var searching = !this.state.searching;
    if (searching) {
      this.searchBar.show();
    } else {
      this.searchBar.hide();
    }
    this.setState({ searching: searching });
    this._startRecognizing(e);
  }

  render() {
    return (
      <SafeAreaView style={styles.root}>
        <SearchBar
          ref={(ref) => this.searchBar = ref}
          hideX={true}
          placeholder={this.state.results[0]}
        />
        <Header
          style={styles.header}
          iconButton={() => {
            this.props.navigation.pop();
          }}
        />
        <SearchButton
          value={this.state.partialResults.map((result, index) => {
            { result }
          })}
          style={styles.searchButton}
          iconType="MaterialIcons"
          iconName="mic"
          onPress={this._onSearchButtonClick.bind(this)}
        />
      </SafeAreaView>
    );
  }
}
const styles = StyleSheet.create({
  root: {
    backgroundColor: "white",
    flex: 1
  },
  header: {
    top: 20,
    left: 0,
    position: "absolute",
    height: 55,
    width: 375
  },
  searchButton: {
    top: 597,
    left: 300,
    position: "absolute",
    height: 57,
    width: 57
  }
});

/*
const DrawerNavigation = DrawerNavigator({
  App: {
    screen: App
  }
});
const StackNavigation = StackNavigator(
  {
    DrawerNavigation: {
      screen: DrawerNavigation
    },
    App: {
      screen: App
    }
  },
  {
    headerMode: "none"
  }
);
*/