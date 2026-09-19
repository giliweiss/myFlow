import { useMemo, useState } from 'react';
import { View, StyleSheet, ScrollView, Text } from 'react-native';
import { useRouter } from 'expo-router';
import {
  ScreenContainer,
  Card,
  ListItem,
  SectionHeader,
  TextField,
  EmptyState,
  LoadingState,
  IconButton,
  Badge,
} from '../../src/components/ui';
import { theme } from '../../src/theme';
import { strings } from '../../src/i18n/he';
import { useExerciseCatalog } from '../../src/hooks/use-exercises';
import { useInstructorExercises } from '../../src/hooks/use-instructor-exercises';
import { filterExercisesBySearch } from '../../src/lib/lesson-form';
import { filterInstructorExercisesBySearch } from '../../src/lib/instructor-exercise-form';
import { levelToDisplay } from '../../src/lib/group-form';
import type { GroupLevel } from '../../src/types/group';

export default function ExercisesCatalogScreen() {
  const router = useRouter();
  const [searchText, setSearchText] = useState('');

  const {
    data: catalogExercises = [],
    isLoading: catalogLoading,
    isError: catalogError,
  } = useExerciseCatalog();

  const {
    data: myExercises = [],
    isLoading: myLoading,
    isError: myError,
  } = useInstructorExercises();

  const filteredCatalog = useMemo(
    () => filterExercisesBySearch(catalogExercises, searchText),
    [catalogExercises, searchText],
  );

  const filteredMine = useMemo(
    () => filterInstructorExercisesBySearch(myExercises, searchText),
    [myExercises, searchText],
  );

  const isLoading = catalogLoading || myLoading;
  const isError = catalogError || myError;

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
        <LoadingState message={strings.common.error} />
      </ScreenContainer>
    );
  }

  return (
    <ScreenContainer paddingHorizontal={false}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.searchContainer}>
          <TextField
            label={strings.lessons.searchExercises}
            placeholder={strings.lessons.searchExercisesPlaceholder}
            value={searchText}
            onChangeText={setSearchText}
          />
        </View>

        <SectionHeader
          title={strings.exercises.approvedCatalog}
          action={<Badge label={strings.exercises.readOnlyBadge} />}
        />
        <Text style={styles.sectionHint}>{strings.exercises.approvedCatalogHint}</Text>

        {filteredCatalog.length === 0 ? (
          <View style={styles.emptySection}>
            <Text style={styles.emptyText}>{strings.lessons.noCatalogResults}</Text>
          </View>
        ) : (
          filteredCatalog.map((item) => (
            <Card
              key={item.id}
              onPress={() => router.push(`/exercises/catalog/${item.id}`)}
              style={styles.card}
            >
              <ListItem
                title={item.name_he}
                subtitle={levelToDisplay(item.difficulty_level as GroupLevel)}
                iconName="BookOpen"
              />
            </Card>
          ))
        )}

        <SectionHeader
          title={strings.exercises.myExercises}
          action={
            <IconButton
              iconName="Plus"
              onPress={() => router.push('/exercises/mine/new')}
            />
          }
        />
        <Text style={styles.sectionHint}>{strings.exercises.myExercisesHint}</Text>

        {filteredMine.length === 0 ? (
          <EmptyState
            title={strings.exercises.noMyExercises}
            message={strings.exercises.createFirstExercise}
            iconName="Dumbbell"
            actionLabel={strings.exercises.newExercise}
            onAction={() => router.push('/exercises/mine/new')}
          />
        ) : (
          filteredMine.map((item) => (
            <Card
              key={item.id}
              onPress={() => router.push(`/exercises/mine/${item.id}`)}
              style={styles.card}
            >
              <ListItem
                title={item.name_he}
                subtitle={levelToDisplay(item.difficulty_level as GroupLevel)}
                iconName="Dumbbell"
                rightContent={<Badge label={strings.exercises.customBadge} />}
              />
            </Card>
          ))
        )}
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    paddingBottom: theme.spacing.xl,
  },

  searchContainer: {
    paddingHorizontal: theme.spacing.md,
    paddingTop: theme.spacing.sm,
    paddingBottom: theme.spacing.md,
  },

  sectionHint: {
    ...theme.typography.caption,
    color: theme.colors.textSecondary,
    paddingHorizontal: theme.spacing.md,
    paddingBottom: theme.spacing.sm,
    textAlign: 'right',
  },

  emptySection: {
    paddingHorizontal: theme.spacing.md,
    paddingBottom: theme.spacing.lg,
  },

  emptyText: {
    ...theme.typography.body,
    color: theme.colors.textSecondary,
    textAlign: 'right',
  },

  card: {
    marginHorizontal: 0,
    borderRadius: 0,
    marginBottom: theme.spacing.xs,
  },
});
