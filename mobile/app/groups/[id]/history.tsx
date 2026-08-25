import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import {
  ScreenContainer,
  Card,
  ListItem,
  EmptyState,
  Badge,
  LoadingState,
} from '../../../src/components/ui';
import { theme } from '../../../src/theme';
import { strings } from '../../../src/i18n/he';
import { useGroupLessons } from '../../../src/hooks/use-lessons';
import { formatLessonDateDisplay } from '../../../src/lib/lesson-form';
import { STATUS_LABELS, STATUS_VARIANTS } from '../../../src/lib/lesson-status';
import type { LessonStatus } from '../../../src/types/lesson';

export default function LessonHistoryScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const groupId = Array.isArray(id) ? id[0] : id;

  const {
    data: lessons = [],
    isLoading,
    isError,
    refetch,
    isRefetching,
  } = useGroupLessons(groupId);

  const handleLessonPress = (lessonId: string) => {
    if (!groupId) {
      return;
    }
    router.push(`/groups/${groupId}/lessons/${lessonId}`);
  };

  if (isLoading) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.loading} />
      </ScreenContainer>
    );
  }

  if (isError) {
    return (
      <ScreenContainer>
        <EmptyState
          title={strings.common.error}
          message={strings.lessons.saveFailed}
          iconName="AlertCircle"
        />
      </ScreenContainer>
    );
  }

  if (lessons.length === 0) {
    return (
      <ScreenContainer>
        <EmptyState
          title={strings.lessons.noLessonHistory}
          message="אין שיעורים בעבר עדיין"
          iconName="Clock"
        />
      </ScreenContainer>
    );
  }

  return (
    <ScreenContainer paddingHorizontal={false}>
      <FlatList
        data={lessons}
        keyExtractor={(item) => item.id}
        refreshControl={
          <RefreshControl refreshing={isRefetching} onRefresh={refetch} />
        }
        renderItem={({ item }) => {
          const status = item.status as LessonStatus;
          const dateLabel = formatLessonDateDisplay(
            item.scheduled_for,
            item.created_at,
          );
          const durationLabel = item.planned_duration_minutes
            ? `${item.planned_duration_minutes} דקות`
            : undefined;

          return (
            <Card style={styles.lessonCard}>
              <ListItem
                title={item.title}
                subtitle={[dateLabel, durationLabel].filter(Boolean).join(' • ')}
                iconName="Calendar"
                onPress={() => handleLessonPress(item.id)}
                rightContent={
                  <Badge
                    label={STATUS_LABELS[status]}
                    variant={STATUS_VARIANTS[status]}
                  />
                }
              />
            </Card>
          );
        }}
        contentContainerStyle={styles.listContent}
        ItemSeparatorComponent={() => <View style={styles.separator} />}
      />
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  listContent: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
  },

  lessonCard: {
    marginBottom: 0,
  },

  separator: {
    height: theme.spacing.sm,
  },
});
