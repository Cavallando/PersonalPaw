import React, {Component} from 'react';
import {Platform, StyleSheet, Text, SafeView} from 'react-native';

//components
import {SearchBar }  from './components/SearchBar/SearchBar.js';

class App extends Component {
  render() {
    return (
      <SafeView>
          <SearchBar />
      </SafeView>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
});

export default App;