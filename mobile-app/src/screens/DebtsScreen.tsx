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

          {/* MVP Feature 1: Debt Tracking - Sample Debt Cards */}
          <VStack space="md">
            <Text size="lg" className="text-white font-semibold">
              Debt Tracking & Management
            </Text>
            
            {/* Sample Credit Card Debt */}
            <Card className="p-4 bg-gray-800/50 border-l-4 border-l-red-500 shadow-sm">
              <VStack space="sm">
                <Text size="sm" className="text-red-400 font-semibold">
                  Credit Card - Chase Sapphire
                </Text>
                <Text size="2xl" className="text-white font-bold">
                  $8,450.00
                </Text>
                <Text size="sm" className="text-gray-300">
                  18.9% APR • $275 min payment
                </Text>
              </VStack>
            </Card>
            
            {/* Sample Personal Loan */}
            <Card className="p-4 bg-gray-800/50 border-l-4 border-l-orange-500 shadow-sm">
              <VStack space="sm">
                <Text size="sm" className="text-orange-400 font-semibold">
                  Personal Loan - Wells Fargo
                </Text>
                <Text size="2xl" className="text-white font-bold">
                  $12,300.00
                </Text>
                <Text size="sm" className="text-gray-300">
                  12.5% APR • $425 min payment
                </Text>
              </VStack>
            </Card>
            
            {/* Add New Debt Button */}
            <Card className="p-4 bg-gray-700/30 border-2 border-dashed border-gray-600 shadow-sm">
              <VStack space="sm" className="items-center">
                <Text size="md" className="text-gray-400 text-center">
                  + Add New Debt
                </Text>
                <Text size="xs" className="text-gray-500 text-center">
                  Credit cards, loans, mortgages, etc.
                </Text>
              </VStack>
            </Card>
          </VStack>

          {/* Debt Management Actions */}
          <Card className="p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
            <VStack space="md">
              <Heading size="lg" className="text-white font-semibold">
                Quick Actions
              </Heading>
              <VStack space="sm">
                <Button variant="outline" className="border-blue-600 bg-blue-700/20">
                  <ButtonText className="text-blue-400">Edit Debt Details</ButtonText>
                </Button>
                <Button variant="outline" className="border-green-600 bg-green-700/20">
                  <ButtonText className="text-green-400">Log Payment</ButtonText>
                </Button>
                <Button variant="outline" className="border-gray-600">
                  <ButtonText className="text-gray-300">View Payment History</ButtonText>
                </Button>
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