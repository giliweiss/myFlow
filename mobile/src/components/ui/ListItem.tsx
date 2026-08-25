import React, { ReactNode } from 'react';
import { View, Pressable, StyleSheet, Text } from 'react-native';
import * as Icons from 'lucide-react-native';
import { theme } from '../../theme';

interface ListItemProps {
  title: string;
  subtitle?: string;
  iconName?: keyof typeof Icons;
  rightContent?: ReactNode;
  onPress?: () => void;
}

export function ListItem({
  title,
  subtitle,
  iconName,
  rightContent,
  onPress,
}: ListItemProps) {
  const IconComponent = iconName ? (Icons as any)[iconName] : null;

  const content = (
    <View style={styles.container}>
      {IconComponent && (
        <View style={styles.iconContainer}>
          <IconComponent size={24} color={theme.colors.primary} strokeWidth={2} />
        </View>
      )}
      <View style={styles.textContainer}>
        <Text style={theme.typography.body}>{title}</Text>
        {subtitle && (
          <Text style={[theme.typography.caption, { marginTop: theme.spacing.xs }]}>
            {subtitle}
          </Text>
        )}
      </View>
      {rightContent && <View style={styles.rightContent}>{rightContent}</View>}
      {onPress && !rightContent && (
        <Icons.ChevronLeft size={20} color={theme.colors.textSecondary} strokeWidth={2} />
      )}
    </View>
  );

  if (onPress) {
    return (
      <Pressable onPress={onPress} style={({ pressed }) => pressed && styles.pressed}>
        {content}
      </Pressable>
    );
  }

  return content;
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row-reverse',
    alignItems: 'center',
    paddingVertical: theme.spacing.md,
    paddingHorizontal: theme.spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },

  pressed: {
    backgroundColor: theme.colors.primaryLight,
  },

  iconContainer: {
    marginLeft: theme.spacing.md,
  },

  textContainer: {
    flex: 1,
  },

  rightContent: {
    marginRight: theme.spacing.md,
  },
});
