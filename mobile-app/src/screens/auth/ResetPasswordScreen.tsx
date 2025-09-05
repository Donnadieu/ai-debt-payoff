import React, { useState } from 'react';
import { ScrollView, Alert } from 'react-native';
import { Box } from '@/components/ui/box';
import { Text } from '@/components/ui/text';
import { Heading } from '@/components/ui/heading';
import { VStack } from '@/components/ui/vstack';
import { Card } from '@/components/ui/card';
import { Button, ButtonText, ButtonSpinner } from '@/components/ui/button';
import { Input, InputField } from '@/components/ui/input';
import { Icon } from '@/components/ui/icon';
import { Mail, ArrowLeft } from 'lucide-react-native';
import { useAuth } from '../../contexts/AuthContext';

interface ResetPasswordScreenProps {
  navigation: any;
}

export default function ResetPasswordScreen({ navigation }: ResetPasswordScreenProps) {
  const [email, setEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [emailSent, setEmailSent] = useState(false);
  
  const { resetPassword } = useAuth();

  const handleResetPassword = async () => {
    if (!email.trim()) {
      Alert.alert('Error', 'Please enter your email address.');
      return;
    }

    if (!email.includes('@')) {
      Alert.alert('Error', 'Please enter a valid email address.');
      return;
    }

    try {
      setIsSubmitting(true);
      await resetPassword(email.trim());
      setEmailSent(true);
    } catch (error: any) {
      Alert.alert('Reset Failed', error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const navigateToLogin = () => {
    navigation.navigate('Login');
  };

  if (emailSent) {
    return (
      <ScrollView className="flex-1" style={{ backgroundColor: '#121212' }}>
        <Box className="flex-1 p-6 pt-20">
          <VStack space="xl">
            {/* Success Header */}
            <VStack space="md" className="items-center">
              <Icon as={Mail} size="3xl" className="text-green-400" />
              <Heading size="2xl" className="text-white font-bold text-center">
                Check Your Email
              </Heading>
              <Text size="md" className="text-gray-300 text-center">
                We've sent password reset instructions to {email}
              </Text>
            </VStack>

            {/* Instructions */}
            <Card className="p-6 bg-gray-800/50 border border-gray-600/50 shadow-lg">
              <VStack space="md">
                <Text size="md" className="text-white font-semibold">
                  What's next?
                </Text>
                <VStack space="sm">
                  <Text size="sm" className="text-gray-300">
                    • Check your email inbox for the reset link
                  </Text>
                  <Text size="sm" className="text-gray-300">
                    • Click the link to create a new password
                  </Text>
                  <Text size="sm" className="text-gray-300">
                    • Return to the app to sign in with your new password
                  </Text>
                </VStack>
                <Text size="xs" className="text-gray-400">
                  Didn't receive the email? Check your spam folder or try again with a different email address.
                </Text>
              </VStack>
            </Card>

            {/* Back to Login */}
            <Button 
              className="bg-blue-600"
              onPress={navigateToLogin}
            >
              <ButtonText className="text-white font-semibold">
                Back to Sign In
              </ButtonText>
            </Button>
          </VStack>
        </Box>
      </ScrollView>
    );
  }

  return (
    <ScrollView className="flex-1" style={{ backgroundColor: '#121212' }}>
      <Box className="flex-1 p-6 pt-20">
        <VStack space="xl">
          {/* Header */}
          <VStack space="md">
            <Button 
              variant="link" 
              size="sm"
              onPress={navigateToLogin}
              className="self-start -ml-2"
            >
              <Icon as={ArrowLeft} size="sm" className="text-blue-400 mr-2" />
              <ButtonText className="text-blue-400">Back to Sign In</ButtonText>
            </Button>
            
            <VStack space="md" className="items-center">
              <Icon as={Mail} size="3xl" className="text-blue-400" />
              <Heading size="2xl" className="text-white font-bold text-center">
                Reset Password
              </Heading>
              <Text size="md" className="text-gray-300 text-center">
                Enter your email address and we'll send you a link to reset your password
              </Text>
            </VStack>
          </VStack>

          {/* Reset Form */}
          <Card className="p-6 bg-gray-800/50 border border-gray-600/50 shadow-lg">
            <VStack space="lg">
              {/* Email Input */}
              <VStack space="sm">
                <Text size="sm" className="text-gray-300 font-medium">
                  Email Address
                </Text>
                <Box className="relative">
                  <Input className="bg-gray-700/50 border-gray-600">
                    <InputField
                      placeholder="Enter your email"
                      value={email}
                      onChangeText={setEmail}
                      keyboardType="email-address"
                      autoCapitalize="none"
                      autoCorrect={false}
                      className="text-white placeholder:text-gray-400"
                    />
                  </Input>
                  <Box className="absolute right-3 top-3">
                    <Icon as={Mail} size="sm" className="text-gray-400" />
                  </Box>
                </Box>
              </VStack>

              {/* Send Reset Email Button */}
              <Button 
                className="bg-blue-600 hover:bg-blue-700"
                onPress={handleResetPassword}
                disabled={isSubmitting}
              >
                {isSubmitting && <ButtonSpinner className="mr-2" />}
                <ButtonText className="text-white font-semibold">
                  {isSubmitting ? 'Sending...' : 'Send Reset Email'}
                </ButtonText>
              </Button>
            </VStack>
          </Card>

          {/* Help Text */}
          <Text size="xs" className="text-gray-400 text-center">
            Remember your password?{' '}
            <Text className="text-blue-400" onPress={navigateToLogin}>
              Sign in instead
            </Text>
          </Text>
        </VStack>
      </Box>
    </ScrollView>
  );
}