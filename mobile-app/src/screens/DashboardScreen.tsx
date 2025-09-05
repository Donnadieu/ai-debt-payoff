import React from 'react';
import { ScrollView } from 'react-native';
import { Box } from '@/components/ui/box';
import { Text } from '@/components/ui/text';
import { Heading } from '@/components/ui/heading';
import { VStack } from '@/components/ui/vstack';
import { HStack } from '@/components/ui/hstack';
import { Card } from '@/components/ui/card';

export default function DashboardScreen() {
  return (
    <ScrollView className="flex-1" style={{ backgroundColor: '#121212' }}>
      <Box className="flex-1 p-4 pt-12">
        <VStack space="lg">
          {/* Header */}
          <VStack space="sm">
            <Heading size="2xl" className="text-typography-900">
              Debt Payoff Dashboard
            </Heading>
            <Text size="md" className="text-typography-600">
              Track your progress toward financial freedom
            </Text>
          </VStack>

          {/* Summary Cards */}
          <VStack space="md">
            <Card className="p-4 bg-background-50 border border-outline-200">
              <VStack space="sm">
                <Text size="sm" className="text-typography-600 font-medium">
                  Total Debt Remaining
                </Text>
                <Heading size="xl" className="text-typography-900">
                  $0.00
                </Heading>
              </VStack>
            </Card>

            <HStack space="md">
              <Card className="flex-1 p-4 bg-background-50 border border-outline-200">
                <VStack space="sm">
                  <Text size="sm" className="text-typography-600 font-medium">
                    Monthly Payment
                  </Text>
                  <Heading size="lg" className="text-typography-900">
                    $0.00
                  </Heading>
                </VStack>
              </Card>

              <Card className="flex-1 p-4 bg-background-50 border border-outline-200">
                <VStack space="sm">
                  <Text size="sm" className="text-typography-600 font-medium">
                    Payoff Date
                  </Text>
                  <Heading size="lg" className="text-typography-900">
                    --
                  </Heading>
                </VStack>
              </Card>
            </HStack>
          </VStack>

          {/* Quick Actions */}
          <VStack space="md">
            <Heading size="lg" className="text-typography-900">
              Quick Actions
            </Heading>
            
            <Card className="p-4 bg-background-50 border border-outline-200">
              <Text size="md" className="text-typography-700">
                Add your debts to get started with your personalized payoff plan
              </Text>
            </Card>
          </VStack>

          {/* Progress Section */}
          <VStack space="md">
            <Heading size="lg" className="text-typography-900">
              Your Progress
            </Heading>
            
            <Card className="p-4 bg-background-50 border border-outline-200">
              <Text size="md" className="text-typography-700">
                Your debt payoff journey will be tracked here
              </Text>
            </Card>
          </VStack>
        </VStack>
      </Box>
    </ScrollView>
  );
}
