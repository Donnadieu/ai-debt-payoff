import React from 'react';
import { ScrollView, Alert } from 'react-native';
import { Box } from '@/components/ui/box';
import { Text } from '@/components/ui/text';
import { Heading } from '@/components/ui/heading';
import { VStack } from '@/components/ui/vstack';
import { Card } from '@/components/ui/card';
import { Button, ButtonText } from '@/components/ui/button';
import { useAuth } from '../contexts/AuthContext';

export default function SettingsScreen() {
  const { user, signOut } = useAuth();

  const handleSignOut = () => {
    Alert.alert(
      'Sign Out',
      'Are you sure you want to sign out?',
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Sign Out', 
          style: 'destructive',
          onPress: async () => {
            try {
              await signOut();
            } catch (error: any) {
              Alert.alert('Error', 'Failed to sign out. Please try again.');
            }
          }
        }
      ]
    );
  };
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

          {/* MVP Feature 2: Payment Strategy Selection */}
          <Card className="p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
            <VStack space="md">
              <Heading size="lg" className="text-white font-semibold">
                Payment Strategy
              </Heading>
              <VStack space="sm">
                {/* Debt Snowball Strategy */}
                <Card className="p-3 bg-blue-900/30 border border-blue-600/50">
                  <VStack space="xs">
                    <Text size="md" className="text-blue-400 font-semibold">
                      ✓ Debt Snowball (Selected)
                    </Text>
                    <Text size="sm" className="text-gray-300">
                      Pay minimums on all debts, put extra toward smallest balance first
                    </Text>
                    <Text size="xs" className="text-blue-300">
                      Psychological wins • Faster motivation • 28 months to debt-free
                    </Text>
                  </VStack>
                </Card>
                
                {/* Debt Avalanche Strategy */}
                <Card className="p-3 bg-gray-700/30 border border-gray-600/50">
                  <VStack space="xs">
                    <Text size="md" className="text-gray-300 font-semibold">
                      Debt Avalanche
                    </Text>
                    <Text size="sm" className="text-gray-400">
                      Pay minimums on all debts, put extra toward highest interest rate first
                    </Text>
                    <Text size="xs" className="text-green-400">
                      Save $1,247 more interest • 26 months to debt-free
                    </Text>
                  </VStack>
                </Card>
                
                <Button className="bg-blue-600">
                  <ButtonText>Switch Strategy</ButtonText>
                </Button>
              </VStack>
            </VStack>
          </Card>
          
          {/* App Preferences */}
          <Card className="p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
            <VStack space="md">
              <Heading size="lg" className="text-white font-semibold">
                App Settings
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

          {/* Account Information */}
          <Card className="p-4 bg-gray-800/50 border border-gray-600/50 shadow-sm">
            <VStack space="md">
              <Heading size="lg" className="text-white font-semibold">
                Account
              </Heading>
              <VStack space="sm">
                <Text size="sm" className="text-gray-300">
                  Signed in as: {user?.email}
                </Text>
                <Text size="xs" className="text-gray-400">
                  Account verified: {user?.emailVerified ? '✓ Yes' : '✗ No'}
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

          {/* Sign Out */}
          <Button 
            className="bg-red-600 hover:bg-red-700"
            onPress={handleSignOut}
          >
            <ButtonText className="text-white font-semibold">
              Sign Out
            </ButtonText>
          </Button>
        </VStack>
      </Box>
    </ScrollView>
  );
}