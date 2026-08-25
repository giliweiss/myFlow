import { TextStyle } from 'react-native';
import { colors } from './tokens';

export const typography = {
  display: {
    fontFamily: 'Rubik_700Bold',
    fontSize: 32,
    lineHeight: 40,
    color: colors.textPrimary,
    writingDirection: 'rtl' as const,
    textAlign: 'right' as const,
  } as TextStyle,

  title: {
    fontFamily: 'Rubik_600SemiBold',
    fontSize: 20,
    lineHeight: 28,
    color: colors.textPrimary,
    writingDirection: 'rtl' as const,
    textAlign: 'right' as const,
  } as TextStyle,

  subtitle: {
    fontFamily: 'Rubik_600SemiBold',
    fontSize: 16,
    lineHeight: 24,
    color: colors.textPrimary,
    writingDirection: 'rtl' as const,
    textAlign: 'right' as const,
  } as TextStyle,

  body: {
    fontFamily: 'Rubik_400Regular',
    fontSize: 14,
    lineHeight: 22,
    color: colors.textPrimary,
    writingDirection: 'rtl' as const,
    textAlign: 'right' as const,
  } as TextStyle,

  caption: {
    fontFamily: 'Rubik_500Medium',
    fontSize: 12,
    lineHeight: 18,
    color: colors.textSecondary,
    writingDirection: 'rtl' as const,
    textAlign: 'right' as const,
  } as TextStyle,
};
