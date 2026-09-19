import { View, StyleSheet, ScrollView, Text } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import {
  ScreenContainer,
  LoadingState,
  Badge,
  Card,
} from '../../../src/components/ui';
import { theme } from '../../../src/theme';
import { strings } from '../../../src/i18n/he';
import { useExercise } from '../../../src/hooks/use-exercises';
import { levelToDisplay } from '../../../src/lib/group-form';
import type { GroupLevel } from '../../../src/types/group';
import { formatCommaList } from '../../../src/lib/group-form';

function DetailRow({ label, value }: { label: string; value: string }) {
  if (!value) {
    return null;
  }

  return (
    <View style={styles.detailRow}>
      <Text style={styles.detailLabel}>{label}</Text>
      <Text style={styles.detailValue}>{value}</Text>
    </View>
  );
}

function BulletList({ title, items }: { title: string; items: string[] }) {
  if (items.length === 0) {
    return null;
  }

  return (
    <View style={styles.listSection}>
      <Text style={styles.detailLabel}>{title}</Text>
      {items.map((item) => (
        <Text key={item} style={styles.bulletItem}>
          • {item}
        </Text>
      ))}
    </View>
  );
}

export default function CatalogExerciseDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { data: exercise, isLoading, isError } = useExercise(id ?? '');

  if (isLoading) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.loading} />
      </ScreenContainer>
    );
  }

  if (isError || !exercise) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.exercises.loadFailed} />
      </ScreenContainer>
    );
  }

  return (
    <ScreenContainer paddingHorizontal={false}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Card style={styles.headerCard}>
          <View style={styles.headerRow}>
            <Text style={theme.typography.title}>{exercise.name_he}</Text>
            <Badge label={strings.exercises.readOnlyBadge} />
          </View>
          {exercise.name_en ? (
            <Text style={styles.subtitle}>{exercise.name_en}</Text>
          ) : null}
        </Card>

        <View style={styles.details}>
          <DetailRow
            label={strings.exercises.difficultyLevel}
            value={levelToDisplay(exercise.difficulty_level as GroupLevel)}
          />
          <DetailRow
            label={strings.exercises.descriptionHe}
            value={exercise.description_he ?? strings.exercises.noDescription}
          />
          <DetailRow
            label={strings.exercises.bodyFocus}
            value={formatCommaList(exercise.body_focus)}
          />
          <DetailRow
            label={strings.exercises.equipment}
            value={formatCommaList(exercise.possible_equipment)}
          />
          <BulletList
            title={strings.exercises.teachingCues}
            items={exercise.teaching_cues_he}
          />
          <BulletList
            title={strings.exercises.commonMistakes}
            items={exercise.common_mistakes_he}
          />
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    paddingBottom: theme.spacing.xl,
  },

  headerCard: {
    marginHorizontal: theme.spacing.md,
    marginTop: theme.spacing.md,
    marginBottom: theme.spacing.sm,
  },

  headerRow: {
    flexDirection: 'row-reverse',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: theme.spacing.sm,
  },

  subtitle: {
    ...theme.typography.caption,
    color: theme.colors.textSecondary,
    marginTop: theme.spacing.xs,
    textAlign: 'right',
  },

  details: {
    paddingHorizontal: theme.spacing.md,
    gap: theme.spacing.md,
  },

  detailRow: {
    gap: theme.spacing.xs,
  },

  detailLabel: {
    ...theme.typography.caption,
    color: theme.colors.textSecondary,
    textAlign: 'right',
  },

  detailValue: {
    ...theme.typography.body,
    color: theme.colors.textPrimary,
    textAlign: 'right',
  },

  listSection: {
    gap: theme.spacing.xs,
  },

  bulletItem: {
    ...theme.typography.body,
    color: theme.colors.textPrimary,
    textAlign: 'right',
  },
});
