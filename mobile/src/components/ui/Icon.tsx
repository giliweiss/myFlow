import React from 'react';
import * as Icons from 'lucide-react-native';
import { colors } from '../../theme/tokens';

export interface IconProps {
  name: keyof typeof Icons;
  size?: number;
  color?: string;
  strokeWidth?: number;
}

export function Icon({ name, size = 24, color = colors.textPrimary, strokeWidth = 2 }: IconProps) {
  // lucide-react-native exports as a namespace of all icons
  // We need to dynamically get the icon component by name
  const IconComponent = (Icons as any)[name];

  if (!IconComponent) {
    console.warn(`Icon "${name}" not found in lucide-react-native`);
    return null;
  }

  return (
    <IconComponent
      size={size}
      color={color}
      strokeWidth={strokeWidth}
    />
  );
}
