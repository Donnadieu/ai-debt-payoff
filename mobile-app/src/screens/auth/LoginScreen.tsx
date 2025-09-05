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
import { Mail, Lock, Eye, EyeOff } from 'lucide-react-native';
import { useAuth } from '../../contexts/AuthContext';

interface LoginScreenProps {
  navigation: any;
}

export default function LoginScreen({ navigation }: LoginScreenProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { signIn } = useAuth();

  const handleSignIn = async () => {
    if (!email.trim() || !password.trim()) {
      Alert.alert('Error', 'Please fill in all fields.');
      return;
    }

    try {
      setIsSubmitting(true);
      await signIn(email.trim(), password);
      // Navigation will be handled by auth state change
    } catch (error: any) {
      Alert.alert('Sign In Failed', error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const navigateToRegister = () => {
    navigation.navigate('Register');
  };

  const navigateToResetPassword = () => {
    navigation.navigate('ResetPassword');
  };

  return (
    <ScrollView className="flex-1" style={{ backgroundColor: '#121212' }}>
      <Box className="flex-1 p-6 pt-20">
        <VStack space="xl">
          {/* Header */}
          <VStack space="md" className="items-center">
            <Icon as={Lock} size="3xl" className="text-blue-400" />
            <Heading size="2xl" className="text-white font-bold text-center">
              Welcome Back
            </Heading>
            <Text size="md" className="text-gray-300 text-center">
              Sign in to continue your debt freedom journey
            </Text>
          </VStack>

          {/* Login Form */}
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

              {/* Password Input */}
              <VStack space="sm">
                <Text size="sm" className="text-gray-300 font-medium">
                  Password
                </Text>
                <Box className="relative">
                  <Input className="bg-gray-700/50 border-gray-600">
                    <InputField
                      placeholder="Enter your password"
                      value={password}
                      onChangeText={setPassword}
                      secureTextEntry={!showPassword}
                      autoCapitalize="none"
                      className="text-white placeholder:text-gray-400"
                    />
                  </Input>
                  <Button
                    variant="link"
                    size="sm"
                    onPress={() => setShowPassword(!showPassword)}
                    className="absolute right-1 top-1"
                  >
                    <Icon 
                      as={showPassword ? EyeOff : Eye} 
                      size="sm" 
                      className="text-gray-400" 
                    />
                  </Button>
                </Box>
              </VStack>

              {/* Forgot Password Link */}
              <Button 
                variant="link" 
                size="sm"
                onPress={navigateToResetPassword}
                className="self-end"
              >
                <ButtonText className="text-blue-400">
                  Forgot Password?
                </ButtonText>
              </Button>

              {/* Sign In Button */}
              <Button 
                className="bg-blue-600 hover:bg-blue-700"
                onPress={handleSignIn}
                disabled={isSubmitting}
              >
                {isSubmitting && <ButtonSpinner className="mr-2" />}
                <ButtonText className="text-white font-semibold">
                  {isSubmitting ? 'Signing In...' : 'Sign In'}
                </ButtonText>
              </Button>
            </VStack>
          </Card>

          {/* Register Link */}
          <VStack space="sm" className="items-center">
            <Text size="sm" className="text-gray-400">
              Don't have an account?
            </Text>
            <Button variant="link" onPress={navigateToRegister}>
              <ButtonText className="text-blue-400 font-semibold">
                Create Account
              </ButtonText>
            </Button>
          </VStack>
        </VStack>
      </Box>
    </ScrollView>
  );
}