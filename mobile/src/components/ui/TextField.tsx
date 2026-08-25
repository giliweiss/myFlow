import React, { useState } from 'react';
import { View, TextInput, StyleSheet, Text } from 'react-native';
import { theme } from '../../theme';

interface TextFieldProps {
  label: string;
  placeholder?: string;
  value: string;
  onChangeText: (text: string) => void;
  multiline?: boolean;
  numberOfLines?: number;
  secureTextEntry?: boolean;
  error?: string;
  editable?: boolean;
}

export function TextField({
  label,
  placeholder,
  value,
  onChangeText,
  multiline = false,
  numberOfLines = 1,
  secureTextEntry = false,
  error,
  editable = true,
}: TextFieldProps) {
  const [isFocused, setIsFocused] = useState(false);

  return (
    <View style={styles.container}>
      <Text style={theme.typography.subtitle}>{label}</Text>
      <TextInput
        style={[
          styles.input,
          isFocused && styles.inputFocused,
          error && styles.inputError,
        ]}
        placeholder={placeholder}
        placeholderTextColor={theme.colors.textSecondary}
        value={value}
        onChangeText={onChangeText}
        multiline={multiline}
        numberOfLines={numberOfLines}
        secureTextEntry={secureTextEntry}
        editable={editable}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
      />
      {error && (
        <Text style={styles.errorText}>{error}</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: theme.spacing.md,
  },

  input: {
    marginTop: theme.spacing.sm,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    borderRadius: theme.radius.md,
    borderWidth: 1,
    borderColor: theme.colors.border,
    backgroundColor: theme.colors.surface,
    fontSize: 14,
    color: theme.colors.textPrimary,
    fontFamily: 'Rubik_400Regular',
    textAlignVertical: 'top',
    textAlign: 'right' as const,
    writingDirection: 'rtl' as const,
  },

  inputFocused: {
    borderColor: theme.colors.primary,
    borderWidth: 2,
  },

  inputError: {
    borderColor: theme.colors.error,
  },

  errorText: {
    marginTop: theme.spacing.xs,
    fontSize: 12,
    color: theme.colors.error,
    fontFamily: 'Rubik_400Regular',
    textAlign: 'right' as const,
    writingDirection: 'rtl' as const,
  },
});
