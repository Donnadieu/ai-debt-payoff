import React from 'react';
import { ScrollView } from 'react-native';
import { Box } from '@/components/ui/box';
import { Text } from '@/components/ui/text';
import { Heading } from '@/components/ui/heading';
import { VStack } from '@/components/ui/vstack';
import { Card } from '@/components/ui/card';
import { Button, ButtonText } from '@/components/ui/button';

export default function SettingsScreen() {
  return (
    <ScrollView className="flex-1" style={{ backgroundColor: '#121212' }}>
      <Box className="flex-1 p-4 pt-12">
        <VStack space="lg">
          {/* Header */}
          <VStack space="sm">
            <Heading size="2xl" className="text-white font-bold">
              Settings
            </Heading>
            <Text size="md" className="text-gray-300">
              Customize your debt payoff experience
            </Text>
          </VStack>

          {/* App Information */}
          <Card className="p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
            <VStack space="md">
              <Heading size="lg" className="text-white font-semibold">
                App Information
              </Heading>
              <VStack space="sm">
                <Text size="md" className="text-gray-300">
                  Version: 1.0.0
                </Text>
                <Text size="md" className="text-gray-300">
                  AI Debt Payoff Planner
                </Text>
              </VStack>
            </VStack>
          </Card>

          {/* Preferences */}
          <Card className="p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
            <VStack space="md">
              <Heading size="lg" className="text-white font-semibold">
                Preferences
              </Heading>
              <VStack space="sm">
                <Button variant="outline" className="justify-start border-gray-600 bg-gray-700/30">
                  <ButtonText className="text-gray-200">Notification Settings</ButtonText>
                </Button>
                <Button variant="outline" className="justify-start border-gray-600 bg-gray-700/30">
                  <ButtonText className="text-gray-200">Theme Settings</ButtonText>
                </Button>
                <Button variant="outline" className="justify-start border-gray-600 bg-gray-700/30">
                  <ButtonText className="text-gray-200">Data Export</ButtonText>
                </Button>
              </VStack>
            </VStack>
          </Card>

          {/* Coming Soon */}
          <Card className="p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
            <VStack space="md">
              <Heading size="lg" className="text-white font-semibold">
                Features Coming Soon
              </Heading>
              <VStack space="sm">
                <Text size="md" className="text-gray-300">
                  • Advanced notification preferences
                </Text>
                <Text size="md" className="text-gray-300">
                  • Multiple data export formats
                </Text>
                <Text size="md" className="text-gray-300">
                  • Custom theme creation
                </Text>
                <Text size="md" className="text-gray-300">
                  • Account synchronization
                </Text>
                <Text size="md" className="text-gray-300">
                  • Goal tracking and milestones
                </Text>
              </VStack>
            </VStack>
          </Card>

          {/* Support */}
          <Card className="p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
            <VStack space="md">
              <Heading size="lg" className="text-white font-semibold">
                Support
              </Heading>
              <VStack space="sm">
                <Button variant="outline" className="justify-start border-gray-600 bg-gray-700/30">
                  <ButtonText className="text-gray-200">Help & FAQ</ButtonText>
                </Button>
                <Button variant="outline" className="justify-start border-gray-600 bg-gray-700/30">
                  <ButtonText className="text-gray-200">Contact Support</ButtonText>
                </Button>
                <Button variant="outline" className="justify-start border-gray-600 bg-gray-700/30">
                  <ButtonText className="text-gray-200">Privacy Policy</ButtonText>
                </Button>
              </VStack>
            </VStack>
          </Card>
        </VStack>
      </Box>
    </ScrollView>
  );
}