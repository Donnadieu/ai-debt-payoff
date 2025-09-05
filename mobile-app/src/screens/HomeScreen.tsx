// Home screen for the debt payoff mobile app

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function HomeScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>AI Debt Payoff Planner</Text>
        <Text style={styles.subtitle}>Welcome to your debt freedom journey!</Text>
        
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Quick Stats</Text>
          <Text style={styles.cardText}>Total Debts: $0</Text>
          <Text style={styles.cardText}>Monthly Payment: $0</Text>
          <Text style={styles.cardText}>Payoff Date: Not calculated</Text>
        </View>
        
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Today's Motivation</Text>
          <Text style={styles.cardText}>
            Every payment brings you closer to financial freedom. Stay committed to your plan!
          </Text>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 30,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
  },
  cardText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
});