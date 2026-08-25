import React from 'react';
import { Pressable, StyleSheet, ActivityIndicator, ViewStyle } from 'react-native';
import { Text } from 'react-native';
import { theme } from '../../theme';

export type ButtonVariant = 'primary' | 'secondary' | 'ghost';

interface ButtonProps {
  label: string;
  onPress?: () => void;
  variant?: ButtonVariant;
  disabled?: boolean;
  loading?: boolean;
  style?: ViewStyle;
}

export function Button({
  label,
  onPress,
  variant = 'primary',
  disabled = false,
  loading = false,
  style,
}: ButtonProps) {
  const isDisabled = disabled || loading;

  return (
    <Pressable
      onPress={onPress}
      disabled={isDisabled}
      style={({ pressed }) => [
        styles.base,
        styles[variant],
        isDisabled && styles.disabled,
        pressed && !isDisabled && styles[`${variant}Pressed`],
        style,
      ]}
    >
      {loading ? (
        <ActivityIndicator
          color={variant === 'primary' ? theme.colors.surface : theme.colors.primary}
          size="small"
        />
      ) : (
        <Text
          style={[
            theme.typography.subtitle,
            styles[`${variant}Label`],
          ]}
        >
          {label}
        </Text>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: {
    paddingVertical: theme.spacing.md,
    paddingHorizontal: theme.spacing.lg,
    borderRadius: theme.radius.md,
    justifyContent: 'center',
    alignItems: 'center',
  },

  primary: {
    backgroundColor: theme.colors.primary,
  },

  primaryPressed: {
    opacity: 0.8,
  },

  primaryLabel: {
    color: theme.colors.surface,
  },

  secondary: {
    backgroundColor: theme.colors.surface,
    borderWidth: 2,
    borderColor: theme.colors.border,
  },

  secondaryPressed: {
    backgroundColor: theme.colors.primaryLight,
  },

  secondaryLabel: {
    color: theme.colors.textPrimary,
  },

  ghost: {
    backgroundColor: 'transparent',
  },

  ghostPressed: {
    backgroundColor: theme.colors.primaryLight,
  },

  ghostLabel: {
    color: theme.colors.primary,
  },

  disabled: {
    opacity: 0.5,
  },
});
