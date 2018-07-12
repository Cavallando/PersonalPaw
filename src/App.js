import React, { Component } from 'react';
import { Platform, StyleSheet, Text, SafeAreaView } from 'react-native';

//components 
import SearchBar from './components/SearchBar/SearchBar.jsx';

export default class App extends Component {
  render() {
    return (
      <SafeAreaView>
        <SearchBar />
      </SafeAreaView>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
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
