import React, { useState } from 'react';
import { ScrollView, Alert } from 'react-native';
import { Box } from '@/components/ui/box';
import { Text } from '@/components/ui/text';
import { Heading } from '@/components/ui/heading';
import { VStack } from '@/components/ui/vstack';
import { HStack } from '@/components/ui/hstack';
import { Card } from '@/components/ui/card';
import { Button, ButtonText, ButtonSpinner } from '@/components/ui/button';
import { Input, InputField } from '@/components/ui/input';
import { Icon } from '@/components/ui/icon';
import { UserPlus, Mail, Lock, Eye, EyeOff, Check } from 'lucide-react-native';
import AntDesign from 'react-native-vector-icons/AntDesign';
import { useAuth } from '../../contexts/AuthContext';

interface RegisterScreenProps {
  navigation: any;
}

export default function RegisterScreen({ navigation }: RegisterScreenProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { signUp, signInWithGoogle, signInWithApple, isLoading } = useAuth();

  const validatePassword = (pwd: string) => {
    return pwd.length >= 6;
  };

  const handleSignUp = async () => {
    if (!email.trim() || !password.trim() || !confirmPassword.trim()) {
      Alert.alert('Error', 'Please fill in all fields.');
      return;
    }

    if (!email.includes('@')) {
      Alert.alert('Error', 'Please enter a valid email address.');
      return;
    }

    if (!validatePassword(password)) {
      Alert.alert('Error', 'Password must be at least 6 characters long.');
      return;
    }

    if (password !== confirmPassword) {
      Alert.alert('Error', 'Passwords do not match.');
      return;
    }

    try {
      setIsSubmitting(true);
      await signUp(email.trim(), password);
      Alert.alert(
        'Account Created',
        'Please check your email to verify your account before signing in.',
        [{ text: 'OK', onPress: () => navigation.navigate('Login') }]
      );
    } catch (error: any) {
      Alert.alert('Registration Failed', error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const navigateToLogin = () => {
    navigation.navigate('Login');
  };

  const handleGoogleSignIn = async () => {
    try {
      await signInWithGoogle();
    } catch (error: any) {
      Alert.alert('Google Sign-In Failed', error.message);
    }
  };

  const handleAppleSignIn = async () => {
    try {
      await signInWithApple();
    } catch (error: any) {
      Alert.alert('Apple Sign-In Failed', error.message);
    }
  };

  return (
    <ScrollView className="flex-1" style={{ backgroundColor: '#121212' }}>
      <Box className="flex-1 p-6 pt-20">
        <VStack space="xl">
          {/* Header */}
          <VStack space="md" className="items-center">
            <Icon as={UserPlus} size="3xl" className="text-green-400" />
            <Heading size="2xl" className="text-white font-bold text-center">
              Create Account
            </Heading>
            <Text size="md" className="text-gray-300 text-center">
              Start your journey to debt freedom today
            </Text>
          </VStack>

          {/* Registration Form */}
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
                      placeholder="Create a password"
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
                {/* Password Requirements */}
                <HStack space="xs" className="items-center">
                  <Icon 
                    as={Check} 
                    size="xs" 
                    className={validatePassword(password) ? "text-green-400" : "text-gray-500"} 
                  />
                  <Text size="xs" className={validatePassword(password) ? "text-green-400" : "text-gray-500"}>
                    At least 6 characters
                  </Text>
                </HStack>
              </VStack>

              {/* Confirm Password Input */}
              <VStack space="sm">
                <Text size="sm" className="text-gray-300 font-medium">
                  Confirm Password
                </Text>
                <Box className="relative">
                  <Input className="bg-gray-700/50 border-gray-600">
                    <InputField
                      placeholder="Confirm your password"
                      value={confirmPassword}
                      onChangeText={setConfirmPassword}
                      secureTextEntry={!showConfirmPassword}
                      autoCapitalize="none"
                      className="text-white placeholder:text-gray-400"
                    />
                  </Input>
                  <Button
                    variant="link"
                    size="sm"
                    onPress={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-1 top-1"
                  >
                    <Icon 
                      as={showConfirmPassword ? EyeOff : Eye} 
                      size="sm" 
                      className="text-gray-400" 
                    />
                  </Button>
                </Box>
                {confirmPassword.length > 0 && (
                  <HStack space="xs" className="items-center">
                    <Icon 
                      as={Check} 
                      size="xs" 
                      className={password === confirmPassword ? "text-green-400" : "text-red-400"} 
                    />
                    <Text size="xs" className={password === confirmPassword ? "text-green-400" : "text-red-400"}>
                      {password === confirmPassword ? "Passwords match" : "Passwords don't match"}
                    </Text>
                  </HStack>
                )}
              </VStack>

              {/* Create Account Button */}
              <Button 
                className="bg-green-600 hover:bg-green-700"
                onPress={handleSignUp}
                disabled={isSubmitting || isLoading}
              >
                {(isSubmitting || isLoading) && <ButtonSpinner className="mr-2" />}
                <ButtonText className="text-white font-semibold">
                  {(isSubmitting || isLoading) ? 'Creating Account...' : 'Create Account'}
                </ButtonText>
              </Button>

              {/* Divider */}
              <VStack space="md" className="items-center">
                <Box className="flex-row items-center w-full">
                  <Box className="flex-1 h-px bg-gray-600" />
                  <Text size="sm" className="text-gray-400 mx-4">or</Text>
                  <Box className="flex-1 h-px bg-gray-600" />
                </Box>
              </VStack>

              {/* Provider Sign-In Buttons */}
              <VStack space="sm" className="items-center">
                <Box className="flex-row space-x-4">
                  {/* Google Sign-In */}
                  <Button 
                    variant="outline"
                    className="border-gray-600 bg-gray-700/50 w-14 h-14 rounded-full"
                    onPress={handleGoogleSignIn}
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <ButtonSpinner />
                    ) : (
                      <AntDesign name="google" size={24} color="white" />
                    )}
                  </Button>

                  {/* Apple Sign-In */}
                  <Button 
                    variant="outline"
                    className="border-gray-600 bg-gray-700/50 w-14 h-14 rounded-full ml-4"
                    onPress={handleAppleSignIn}
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <ButtonSpinner />
                    ) : (
                      <AntDesign name="apple1" size={24} color="white" />
                    )}
                  </Button>
                </Box>
              </VStack>
            </VStack>
          </Card>

          {/* Login Link */}
          <VStack space="sm" className="items-center">
            <Text size="sm" className="text-gray-400">
              Already have an account?
            </Text>
            <Button variant="link" onPress={navigateToLogin}>
              <ButtonText className="text-blue-400 font-semibold">
                Sign In
              </ButtonText>
            </Button>
          </VStack>
        </VStack>
      </Box>
    </ScrollView>
  );
}