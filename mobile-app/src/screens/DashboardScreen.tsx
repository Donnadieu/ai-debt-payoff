import React from 'react';
import { ScrollView } from 'react-native';
import { Box } from '@/components/ui/box';
import { Text } from '@/components/ui/text';
import { Heading } from '@/components/ui/heading';
import { VStack } from '@/components/ui/vstack';
import { HStack } from '@/components/ui/hstack';
import { Card } from '@/components/ui/card';
import { Button, ButtonText } from '@/components/ui/button';
import { Icon } from '@/components/ui/icon';
import { CreditCard, TrendingDown, Calendar, Plus, Target, ArrowUp, DollarSign } from 'lucide-react-native';

export default function DashboardScreen() {
  return (
    <ScrollView className="flex-1" style={{ backgroundColor: '#121212' }}>
      <Box className="flex-1 p-4 pt-12">
        <VStack space="lg">
          {/* Header */}
          <Box className="bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl p-6 mb-2">
            <VStack space="sm">
              <HStack space="sm" className="items-center">
                <Icon as={Target} size="xl" className="text-gray-900" />
                <Heading size="xl" className="text-gray-900 font-bold">
                  AI Debt Freedom
                </Heading>
              </HStack>
              <Text size="md" className="text-gray-800 font-semibold">
                You're on your way to freedom 💪
              </Text>
            </VStack>
          </Box>

          {/* Summary Cards */}
          <VStack space="md">
            {/* Main Debt Card */}
            <Card className="p-5 bg-gray-800/50 border-l-4 border-l-orange-500 shadow-sm">
              <VStack space="sm">
                <HStack space="sm" className="items-center">
                  <Icon as={CreditCard} size="sm" className="text-orange-400" />
                  <Text size="sm" className="text-gray-300 font-semibold">
                    Total Debt Remaining
                  </Text>
                </HStack>
                <Heading size="2xl" className="text-white">
                  $0.00
                </Heading>
                <Text size="sm" className="text-gray-400">
                  Add debts to see your total
                </Text>
              </VStack>
            </Card>

            <HStack space="md">
              <Card className="flex-1 p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
                <VStack space="sm">
                  <HStack space="xs" className="items-center">
                    <Icon as={DollarSign} size="xs" className="text-blue-400" />
                    <Text size="sm" className="text-gray-300 font-medium">
                      Monthly Payment
                    </Text>
                  </HStack>
                  <Heading size="lg" className="text-white">
                    $0.00
                  </Heading>
                </VStack>
              </Card>

              <Card className="flex-1 p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
                <VStack space="sm">
                  <HStack space="xs" className="items-center">
                    <Icon as={Calendar} size="xs" className="text-green-400" />
                    <Text size="sm" className="text-gray-300 font-medium">
                      Payoff Date
                    </Text>
                  </HStack>
                  <Heading size="lg" className="text-white">
                    --
                  </Heading>
                </VStack>
              </Card>
            </HStack>
          </VStack>

          {/* Quick Actions */}
          <VStack space="md">
            <HStack space="sm" className="items-center">
              <Icon as={ArrowUp} size="sm" className="text-primary-600" />
              <Heading size="lg" className="text-typography-900">
                Quick Actions
              </Heading>
            </HStack>
            
            <VStack space="sm">
              <Button className="bg-primary-600 hover:bg-primary-700 active:bg-primary-800 rounded-xl p-4">
                <HStack space="sm" className="items-center">
                  <Icon as={Plus} size="sm" className="text-primary-50" />
                  <ButtonText className="text-primary-50 font-semibold">
                    Add Your First Debt
                  </ButtonText>
                </HStack>
              </Button>
              
              <Button variant="outline" className="border-primary-300 rounded-xl p-4">
                <HStack space="sm" className="items-center">
                  <Icon as={TrendingDown} size="sm" className="text-primary-600" />
                  <ButtonText className="text-primary-700 font-medium">
                    View Payoff Strategies
                  </ButtonText>
                </HStack>
              </Button>
            </VStack>
          </VStack>

          {/* Progress Section */}
          <VStack space="md">
            <HStack space="sm" className="items-center">
              <Icon as={Target} size="sm" className="text-gray-400" />
              <Heading size="lg" className="text-typography-900">
                Your Progress
              </Heading>
            </HStack>
            
            <Card className="p-5 bg-gray-800/50 border border-gray-600/50 shadow-sm rounded-xl">
              <VStack space="md" className="items-center">
                <Icon as={Target} size="2xl" className="text-blue-400" />
                <Text size="lg" className="text-white font-semibold text-center">
                  Ready to Start Your Journey?
                </Text>
                <Text size="sm" className="text-gray-300 text-center">
                  Add your debts to see progress charts, payoff timelines, and motivational insights
                </Text>
              </VStack>
            </Card>
          </VStack>
        </VStack>
      </Box>
    </ScrollView>
  );
}
