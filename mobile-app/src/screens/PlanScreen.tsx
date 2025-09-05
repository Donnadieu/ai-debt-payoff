// Payoff plan screen

import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function PlanScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.content}>
        <Text style={styles.title}>Payoff Plan</Text>
        
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Strategy Comparison</Text>
          <Text style={styles.cardText}>
            Add your debts first to see personalized payoff strategies.
          </Text>
        </View>
        
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Snowball vs Avalanche</Text>
          <Text style={styles.cardText}>
            • Snowball: Pay smallest balances first for quick wins{'\n'}
            • Avalanche: Pay highest interest rates first to save money{'\n'}
            • We'll show you which strategy works best for your situation
          </Text>
        </View>
      </ScrollView>
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
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
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
    lineHeight: 20,
  },
});