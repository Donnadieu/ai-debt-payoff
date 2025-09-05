import React from 'react';
import { ScrollView } from 'react-native';
import { Box } from '@/components/ui/box';
import { Text } from '@/components/ui/text';
import { Heading } from '@/components/ui/heading';
import { VStack } from '@/components/ui/vstack';
import { Card } from '@/components/ui/card';
import { Button, ButtonText } from '@/components/ui/button';

export default function DebtsScreen() {
  return (
    <ScrollView className="flex-1" style={{ backgroundColor: '#121212' }}>
      <Box className="flex-1 p-4 pt-12">
        <VStack space="lg">
          {/* Header */}
          <VStack space="sm">
            <Heading size="2xl" className="text-white font-bold">
              My Debts
            </Heading>
            <Text size="md" className="text-gray-300">
              Manage and track all your debts in one place
            </Text>
          </VStack>

          {/* Empty State */}
          <Card className="p-6 bg-gray-800/50 border border-gray-600/50 shadow-sm">
            <VStack space="md" className="items-center">
              <Heading size="lg" className="text-white font-semibold text-center">
                No debts added yet
              </Heading>
              <Text size="md" className="text-gray-300 text-center">
                Add your debts to start creating your personalized payoff plan.
              </Text>
              <Button>
                <ButtonText>Add Your First Debt</ButtonText>
              </Button>
            </VStack>
          </Card>

          {/* Getting Started Guide */}
          <Card className="p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
            <VStack space="md">
              <Heading size="lg" className="text-white font-semibold">
                Get Started
              </Heading>
              <VStack space="sm">
                <Text size="md" className="text-gray-300">
                  • Add each debt with balance, interest rate, and minimum payment
                </Text>
                <Text size="md" className="text-gray-300">
                  • Include credit cards, loans, and other debts
                </Text>
                <Text size="md" className="text-gray-300">
                  • The app will calculate the optimal payoff strategy
                </Text>
              </VStack>
            </VStack>
          </Card>

          {/* Strategy Information */}
          <Card className="p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
            <VStack space="md">
              <Heading size="lg" className="text-white font-semibold">
                Payoff Strategies
              </Heading>
              <VStack space="sm">
                <Text size="md" className="text-gray-300">
                  <Text className="font-semibold text-blue-400">Debt Snowball:</Text> Pay minimums on all debts, put extra toward smallest balance
                </Text>
                <Text size="md" className="text-gray-300">
                  <Text className="font-semibold text-green-400">Debt Avalanche:</Text> Pay minimums on all debts, put extra toward highest interest rate
                </Text>
              </VStack>
            </VStack>
          </Card>
        </VStack>
      </Box>
    </ScrollView>
  );
}