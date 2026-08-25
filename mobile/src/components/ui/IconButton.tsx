import React from 'react';
import { Pressable, StyleSheet } from 'react-native';
import * as Icons from 'lucide-react-native';
import { theme } from '../../theme';

interface IconButtonProps {
  iconName: keyof typeof Icons;
  onPress?: () => void;
  size?: number;
  color?: string;
  disabled?: boolean;
}

export function IconButton({
  iconName,
  onPress,
  size = 24,
  color = theme.colors.primary,
  disabled = false,
}: IconButtonProps) {
  const IconComponent = (Icons as any)[iconName];

  if (!IconComponent) {
    return null;
  }

  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.button,
        pressed && !disabled && styles.pressed,
        disabled && styles.disabled,
      ]}
    >
      <IconComponent size={size} color={color} strokeWidth={2} />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    width: 40,
    height: 40,
    borderRadius: theme.radius.full,
    justifyContent: 'center',
    alignItems: 'center',
  },

  pressed: {
    backgroundColor: theme.colors.primaryLight,
  },

  disabled: {
    opacity: 0.5,
  },
});
