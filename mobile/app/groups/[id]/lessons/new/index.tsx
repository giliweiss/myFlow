import { View, StyleSheet, ScrollView, Text } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { ScreenContainer, Card, LoadingState } from '../../../../../src/components/ui';
import { theme } from '../../../../../src/theme';
import { strings } from '../../../../../src/i18n/he';
import { useGroup } from '../../../../../src/hooks/use-groups';

export default function BuildLessonModeScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const groupId = Array.isArray(id) ? id[0] : id;

  const { data: group, isLoading, isError } = useGroup(groupId);

  const handleManualPress = () => {
    if (!groupId) {
      return;
    }
    router.push(`/groups/${groupId}/lessons/new/manual`);
  };

  const handleAiPress = () => {
    if (!groupId) {
      return;
    }
    router.push(`/groups/${groupId}/lessons/new/ai`);
  };

  if (isLoading) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.loading} />
      </ScreenContainer>
    );
  }

  if (isError || !group) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.error} />
      </ScreenContainer>
    );
  }

  return (
    <ScreenContainer paddingHorizontal={false}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Text style={[theme.typography.body, styles.contextText]}>
          {group.name} • {group.typical_duration_minutes} {strings.lessons.duration}
        </Text>

        <Card onPress={handleManualPress} style={styles.modeCard}>
          <View style={styles.cardContent}>
            <Text style={theme.typography.title}>{strings.lessons.buildModeManual}</Text>
            <Text style={[theme.typography.body, styles.cardDescription]}>
              {strings.lessons.buildModeManualDesc}
            </Text>
          </View>
        </Card>

        <Card onPress={handleAiPress} style={styles.modeCard}>
          <View style={styles.cardContent}>
            <Text style={theme.typography.title}>{strings.lessons.buildModeAi}</Text>
            <Text style={[theme.typography.body, styles.cardDescription]}>
              {strings.lessons.buildModeAiDesc}
            </Text>
            <Text style={[theme.typography.caption, styles.disclaimer]}>
              {strings.lessons.aiCatalogDisclaimer}
            </Text>
          </View>
        </Card>
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
  },

  contextText: {
    textAlign: 'right',
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.lg,
  },

  modeCard: {
    marginBottom: theme.spacing.md,
  },

  cardContent: {
    alignItems: 'flex-end',
  },

  cardDescription: {
    marginTop: theme.spacing.sm,
    color: theme.colors.textSecondary,
    textAlign: 'right',
  },

  disclaimer: {
    marginTop: theme.spacing.md,
    color: theme.colors.textSecondary,
    textAlign: 'right',
  },
});
