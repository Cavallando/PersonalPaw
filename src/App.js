import React, { Component } from "react";
import Header from "./components/Header";
import SearchButton from "./components/SearchButton";
import { SafeAreaView, View, Text, StyleSheet } from "react-native";

//imported modules
import SearchBar from 'react-native-searchbar';
import { Dialogflow_V2 } from "react-native-dialogflow"

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searching: false,
    }
    Dialogflow_V2.setConfiguration(
      "client-access@personalpaw.iam.gserviceaccount.com",
      '-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCn6KNqYuGO50Z3\n342LYW7ICapmFmafRiN8iXNZvNnxk2hqN6mLHmhjMp7KxHUsnbJ6D+IE9aog1obi\nnjhfOcNueLHaz5CP8Efm5TORQnClqpmdsnx4mF/U7tpfynhSkmJoWjXWxTZbbBro\n6Y4BCH8/9SfFWSnKxAcwAwjkpkZANVZmclqu3pig7BTZOPuFpyCFOpmWvr16f4Jt\nyGTk7c1/Xx4qrZrmI+plwSJaVIfAhlgWjv5zoNt0M1xxfRSHYAQU11wAk+YXFKl4\nX9QlYyT5/3jO6gU/fwQrear4rclF6Y1nRGn7qz/5GN+m6fL4V8fQO44TuQx2Z+CP\nl5klxr4hAgMBAAECggEABejLm4poWtGr6rsc7atbrUGd1CL0sKVUyWTDAQUC/JwO\nADL+Tg2faeJVsVgxsYTJS790Wm1U8/vo2l/sJvnO9Xvc8pD8ivxPY4Jsiq+2bDYx\nWtn1xH7EXKedWuKy0mEhgn+uRmVBcP1AgzL5EvM8G0GjCTCGpoK4qAlrTjTF4yuO\nxkBh5BQymWP53N5P1556eivYymHUaqImtcQ9RW8Pz6SNeDGyXnV7kmTLBQ6HnlwQ\ni/ruHoiHiEJlFV7QxEGdWuDcVsZkcHjojU7geqtHOudQ3nQQJftnpE86kaToDTcU\nKF/5P+HK3AUkAxqBRbfCtLef4xPfH3QG8H6BwNSYKwKBgQDajVshXMU5mo2Mpjqn\nsjOMOetnHw2omv2jksBEfnb/BPHJsV78SapDzm09C05QGy1KxQ5YwWNjQy3GAlnG\nl9urpIg04315uN1Y9B9313jS4JHtAyOvFUdUerf0hUE0EQu6HehDqFIuo/kFr9uh\nn+5l0vUFn/F+W6dCpRzYTSsPrwKBgQDErdeqeuDbb4ZLSFb8UUeBWojcbKKCM/a0\nofz3wikyZxMGzvk0itgZs8Gen9Hr2f4bBU9bOb5EU6i0tISu/S6XwnlOHJ4yVb3/\nvzICyQfpMWWUepe1jm+q1qyjUa+LQmSVBqPV+/5cjKzci9ZH/1aF14CDmgrneLB6\nyPdeTfEzLwKBgQCBUrvmFfsuhuHTpFl4+d2+0FcXgiyW5H/J1wCmhx7q8IYSjz5h\nk0WJMhE52gLRLAO1Br3ijyy8g/gF/0YYWavG+WkPwr1w1Y9FH8+vHnWEcxZmZUEs\nTS8UMjnAG0nmAWArFZ9myac3qhek4dbY4MY0wovydB52Ys2qhgF3jNI6SQKBgCg9\nrW+rHpCnO+HxViLf+nJj9Las338mZKbGsfx7VHSElGcDOAfhFKAFoGr1Jj1MZ+pd\nZsQyh1RxjYYTnUY0dTEF0E4EGvYPhwVpuDDLsvuqaK89egbissRQkhgEYZdrqSq4\nphLlMUD8Y23oippGiwxtcFT80phToEAvGDXKWrxvAoGBAIStMhi3kt4M/ZeVWqV0\nQImUzUZGj6KjCHyRCzKgsbh5SfcKGV8GuvftffbHL1lS/MHgPxhQ9dCEBL/FKMF4\npR8ybOo1KyRnYKdgYRvIQcHq9YQBVRJ0a24DJhuzZon6E0sioSzm2/qio+NCwVy7\nowA/IhKopQ9tK93e7/0SWgxQ\n-----END PRIVATE KEY-----\n',
      Dialogflow_V2.LANG_ENGLISH,
      'personalpaw'
    );
  }

  _onSearchButtonClick(e) {
    console.log("in here");
    var searching = !this.state.searching;
    if (searching) {
      this.searchBar.show();
    } else {
      this.searchBar.hide();
    }
    this.setState({ searching: searching });
    Dialogflow_V2.startListening(result => {
      console.log(result);
    }, error => {
      console.log(error);
    })
  }

  render() {
    return (
      <SafeAreaView style={styles.root}>
        <SearchBar
          ref={(ref) => this.searchBar = ref}
          hideX={true}
        />
        <Header
          style={styles.header}
          iconButton={() => {
            this.props.navigation.pop();
          }}
        />
        <SearchButton
          style={styles.searchButton}
          iconType="MaterialIcons"
          iconName="mic"
          onPress={this._onSearchButtonClick.bind(this) }
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