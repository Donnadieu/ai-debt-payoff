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
    <ScrollView className="flex-1 bg-background">
      <Box className="flex-1 p-4 pt-12">
        <VStack space="lg">
          {/* Header */}
          <VStack space="sm">
            <Heading size="2xl" className="text-typography-900">
              Settings
            </Heading>
            <Text size="md" className="text-typography-600">
              Customize your debt payoff experience
            </Text>
          </VStack>

          {/* App Information */}
          <Card className="p-4">
            <VStack space="md">
              <Heading size="lg" className="text-typography-900">
                App Information
              </Heading>
              <VStack space="sm">
                <Text size="md" className="text-typography-700">
                  Version: 1.0.0
                </Text>
                <Text size="md" className="text-typography-700">
                  AI Debt Payoff Planner
                </Text>
              </VStack>
            </VStack>
          </Card>

          {/* Preferences */}
          <Card className="p-4">
            <VStack space="md">
              <Heading size="lg" className="text-typography-900">
                Preferences
              </Heading>
              <VStack space="sm">
                <Button variant="outline" className="justify-start">
                  <ButtonText>Notification Settings</ButtonText>
                </Button>
                <Button variant="outline" className="justify-start">
                  <ButtonText>Theme Settings</ButtonText>
                </Button>
                <Button variant="outline" className="justify-start">
                  <ButtonText>Data Export</ButtonText>
                </Button>
              </VStack>
            </VStack>
          </Card>

          {/* Coming Soon */}
          <Card className="p-4">
            <VStack space="md">
              <Heading size="lg" className="text-typography-900">
                Features Coming Soon
              </Heading>
              <VStack space="sm">
                <Text size="md" className="text-typography-700">
                  • Advanced notification preferences
                </Text>
                <Text size="md" className="text-typography-700">
                  • Multiple data export formats
                </Text>
                <Text size="md" className="text-typography-700">
                  • Custom theme creation
                </Text>
                <Text size="md" className="text-typography-700">
                  • Account synchronization
                </Text>
                <Text size="md" className="text-typography-700">
                  • Goal tracking and milestones
                </Text>
              </VStack>
            </VStack>
          </Card>

          {/* Support */}
          <Card className="p-4">
            <VStack space="md">
              <Heading size="lg" className="text-typography-900">
                Support
              </Heading>
              <VStack space="sm">
                <Button variant="outline" className="justify-start">
                  <ButtonText>Help & FAQ</ButtonText>
                </Button>
                <Button variant="outline" className="justify-start">
                  <ButtonText>Contact Support</ButtonText>
                </Button>
                <Button variant="outline" className="justify-start">
                  <ButtonText>Privacy Policy</ButtonText>
                </Button>
              </VStack>
            </VStack>
          </Card>
        </VStack>
      </Box>
    </ScrollView>
  );
}