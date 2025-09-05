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
            <Heading size="2xl" className="text-typography-900">
              My Debts
            </Heading>
            <Text size="md" className="text-typography-600">
              Manage and track all your debts in one place
            </Text>
          </VStack>

          {/* Empty State */}
          <Card className="p-6 bg-background-50 border border-outline-200">
            <VStack space="md" className="items-center">
              <Heading size="lg" className="text-typography-900 text-center">
                No debts added yet
              </Heading>
              <Text size="md" className="text-typography-600 text-center">
                Add your debts to start creating your personalized payoff plan.
              </Text>
              <Button className="mt-4 bg-primary-600">
                <ButtonText className="text-white">Add Your First Debt</ButtonText>
              </Button>
            </VStack>
          </Card>

          {/* Getting Started Guide */}
          <Card className="p-4 bg-background-50 border border-outline-200">
            <VStack space="md">
              <Heading size="lg" className="text-typography-900">
                Get Started
              </Heading>
              <VStack space="sm">
                <Text size="md" className="text-typography-700">
                  • Add each debt with balance, interest rate, and minimum payment
                </Text>
                <Text size="md" className="text-typography-700">
                  • Include credit cards, loans, and other debts
                </Text>
                <Text size="md" className="text-typography-700">
                  • The app will calculate the optimal payoff strategy
                </Text>
              </VStack>
            </VStack>
          </Card>

          {/* Strategy Information */}
          <Card className="p-4 bg-background-50 border border-outline-200">
            <VStack space="md">
              <Heading size="lg" className="text-typography-900">
                Payoff Strategies
              </Heading>
              <VStack space="sm">
                <Text size="md" className="text-typography-700">
                  <Text className="font-semibold">Debt Snowball:</Text> Pay minimums on all debts, put extra toward smallest balance
                </Text>
                <Text size="md" className="text-typography-700">
                  <Text className="font-semibold">Debt Avalanche:</Text> Pay minimums on all debts, put extra toward highest interest rate
                </Text>
              </VStack>
            </VStack>
          </Card>
        </VStack>
      </Box>
    </ScrollView>
  );
}