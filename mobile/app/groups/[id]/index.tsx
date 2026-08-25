import { View, StyleSheet, ScrollView, Text } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import {
  ScreenContainer,
  Card,
  Button,
  Badge,
  LoadingState,
} from '../../../src/components/ui';
import { theme } from '../../../src/theme';
import { strings } from '../../../src/i18n/he';
import { useGroup } from '../../../src/hooks/use-groups';
import { levelToDisplay } from '../../../src/lib/group-form';

export default function GroupDetailScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const groupId = Array.isArray(id) ? id[0] : id;

  const { data: group, isLoading, isError } = useGroup(groupId);

  const handleBuildLesson = () => {
    if (!groupId) {
      return;
    }
    router.push(`/groups/${groupId}/lessons/new`);
  };

  const handleLessonHistory = () => {
    if (!groupId) {
      return;
    }
    router.push(`/groups/${groupId}/history`);
  };

  const handleSettings = () => {
    if (!groupId) {
      return;
    }
    router.push(`/groups/${groupId}/settings`);
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
        <Card style={styles.summaryCard}>
          <View style={styles.summaryContent}>
            <Text style={theme.typography.title}>{group.name}</Text>
            <Text style={[theme.typography.body, styles.level]}>
              {strings.groups.groupLevel}: {levelToDisplay(group.level)}
            </Text>
            <Text style={[theme.typography.body, styles.duration]}>
              {strings.groups.typicalDuration}: {group.typical_duration_minutes} דקות
            </Text>

            <View style={styles.tagsSection}>
              <Text style={[theme.typography.caption, styles.tagsLabel]}>
                {strings.groups.equipment}
              </Text>
              <View style={styles.tagsList}>
                {group.available_equipment.map((equip, idx) => (
                  <Badge key={idx} label={equip} style={styles.tag} />
                ))}
              </View>
            </View>
          </View>
        </Card>

        <View style={styles.actionsSection}>
          <Button
            label={strings.groups.hubBuildLesson}
            onPress={handleBuildLesson}
            variant="primary"
            style={styles.actionButton}
          />
          <Button
            label={strings.groups.hubLessonHistory}
            onPress={handleLessonHistory}
            variant="primary"
            style={styles.actionButton}
          />
          <Button
            label={strings.groups.hubSettings}
            onPress={handleSettings}
            variant="primary"
            style={styles.actionButton}
          />
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
  },

  summaryCard: {
    marginBottom: theme.spacing.lg,
  },

  summaryContent: {
    alignItems: 'flex-end',
  },

  level: {
    marginTop: theme.spacing.sm,
    color: theme.colors.textSecondary,
  },

  duration: {
    marginTop: theme.spacing.xs,
    color: theme.colors.textSecondary,
  },

  tagsSection: {
    marginTop: theme.spacing.lg,
    alignItems: 'flex-end',
  },

  tagsLabel: {
    marginBottom: theme.spacing.sm,
  },

  tagsList: {
    flexDirection: 'row-reverse',
    flexWrap: 'wrap',
    gap: theme.spacing.sm,
  },

  tag: {
    marginVertical: theme.spacing.xs,
  },

  actionsSection: {
    gap: theme.spacing.md,
    marginBottom: theme.spacing.lg,
  },

  actionButton: {
    width: '100%',
  },
});
