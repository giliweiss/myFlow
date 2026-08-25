import { View, StyleSheet, ScrollView, Text } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { ScreenContainer, Button, Card } from '../../../../../src/components/ui';
import { theme } from '../../../../../src/theme';
import { strings } from '../../../../../src/i18n/he';

export default function AiBuildLessonStubScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const groupId = Array.isArray(id) ? id[0] : id;

  const handleSwitchToManual = () => {
    if (!groupId) {
      return;
    }
    router.replace(`/groups/${groupId}/lessons/new/manual`);
  };

  return (
    <ScreenContainer paddingHorizontal={false}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Card style={styles.comingSoonCard}>
          <View style={styles.cardContent}>
            <Text style={theme.typography.title}>{strings.lessons.aiComingSoon}</Text>
            <Text style={[theme.typography.body, styles.message]}>
              {strings.lessons.aiComingSoonMessage}
            </Text>
          </View>
        </Card>

        <View style={styles.previewFields}>
          <Text style={theme.typography.subtitle}>{strings.lessons.primaryGoal}</Text>
          <Text style={[theme.typography.body, styles.previewPlaceholder]}>
            {strings.lessons.primaryGoal}
          </Text>

          <Text style={[theme.typography.subtitle, styles.previewLabel]}>
            {strings.lessons.lessonNotes}
          </Text>
          <Text style={[theme.typography.body, styles.previewPlaceholder]}>
            {strings.lessons.lessonNotes}
          </Text>
        </View>

        <Text style={[theme.typography.caption, styles.disclaimer]}>
          {strings.lessons.aiCatalogDisclaimer}
        </Text>

        <Button
          label={strings.lessons.switchToManual}
          onPress={handleSwitchToManual}
          style={styles.manualButton}
        />

        <Button
          label={strings.common.comingSoon}
          disabled
          variant="secondary"
          style={styles.generateButton}
        />
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
  },

  comingSoonCard: {
    marginBottom: theme.spacing.lg,
  },

  cardContent: {
    alignItems: 'flex-end',
  },

  message: {
    marginTop: theme.spacing.sm,
    color: theme.colors.textSecondary,
    textAlign: 'right',
  },

  previewFields: {
    marginBottom: theme.spacing.lg,
    alignItems: 'flex-end',
  },

  previewLabel: {
    marginTop: theme.spacing.md,
  },

  previewPlaceholder: {
    marginTop: theme.spacing.sm,
    color: theme.colors.textSecondary,
    textAlign: 'right',
  },

  disclaimer: {
    textAlign: 'right',
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.lg,
  },

  manualButton: {
    marginBottom: theme.spacing.md,
  },

  generateButton: {
    marginBottom: theme.spacing.lg,
  },
});
