import { useState } from 'react';
import { View, StyleSheet, Text, ScrollView } from 'react-native';
import { ScreenContainer, Button, TextField, Card } from '../../src/components/ui';
import { theme } from '../../src/theme';
import { strings } from '../../src/i18n/he';

export default function SignupScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignup = async () => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setLoading(false);
  };

  return (
    <ScreenContainer paddingHorizontal={false}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.container}>
          <View style={styles.header}>
            <Text style={[theme.typography.display, styles.title]}>
              {strings.auth.signup}
            </Text>
          </View>

          <Card style={styles.formCard}>
            <TextField
              label={strings.auth.email}
              placeholder="your@email.com"
              value={email}
              onChangeText={setEmail}
            />
            <TextField
              label={strings.auth.password}
              placeholder="••••••••"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
            />
            <TextField
              label={strings.auth.confirmPassword}
              placeholder="••••••••"
              value={confirmPassword}
              onChangeText={setConfirmPassword}
              secureTextEntry
            />
            <Button
              label={strings.auth.signupButtonLabel}
              onPress={handleSignup}
              loading={loading}
              style={styles.submitButton}
            />
          </Card>

          <View style={styles.footer}>
            <Text style={[theme.typography.body, styles.footerText]}>
              {strings.auth.alreadyHaveAccount}{' '}
              <Text style={styles.footerLink}>{strings.auth.login}</Text>
            </Text>
          </View>
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    flexGrow: 1,
  },

  container: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: theme.spacing.md,
  },

  header: {
    marginBottom: theme.spacing.xxl,
    alignItems: 'center',
  },

  title: {
    textAlign: 'center',
  },

  formCard: {
    marginBottom: theme.spacing.xl,
  },

  submitButton: {
    marginTop: theme.spacing.md,
  },

  footer: {
    alignItems: 'center',
  },

  footerText: {
    color: theme.colors.textSecondary,
  },

  footerLink: {
    color: theme.colors.primary,
    fontFamily: 'Rubik_600SemiBold',
  },
});
