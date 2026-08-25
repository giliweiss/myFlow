import { View, StyleSheet, FlatList } from 'react-native';
import { useRouter } from 'expo-router';
import {
  ScreenContainer,
  Card,
  ListItem,
  EmptyState,
  IconButton,
  LoadingState,
} from '../../src/components/ui';
import { theme } from '../../src/theme';
import { strings } from '../../src/i18n/he';
import { useGroups } from '../../src/hooks/use-groups';
import { levelToDisplay } from '../../src/lib/group-form';

export default function GroupsListScreen() {
  const router = useRouter();
  const { data: groups = [], isLoading, isError } = useGroups();
  const hasGroups = groups.length > 0;

  const handleCreateGroup = () => {
    router.push('/groups/new');
  };

  const handleSelectGroup = (groupId: string) => {
    router.push(`/groups/${groupId}`);
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
        <LoadingState message={strings.common.error} />
      </ScreenContainer>
    );
  }

  return (
    <ScreenContainer>
      {!hasGroups ? (
        <EmptyState
          title={strings.groups.noGroups}
          message={strings.groups.createFirstGroup}
          iconName="Users"
          actionLabel={strings.groups.newGroup}
          onAction={handleCreateGroup}
        />
      ) : (
        <View style={styles.container}>
          <FlatList
            data={groups}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <Card
                onPress={() => handleSelectGroup(item.id)}
                style={styles.groupCard}
              >
                <ListItem
                  title={item.name}
                  subtitle={levelToDisplay(item.level)}
                  iconName="Users"
                  rightContent={
                    <View style={styles.chevron} />
                  }
                />
              </Card>
            )}
            scrollEnabled={false}
            ItemSeparatorComponent={() => <View style={styles.separator} />}
          />
          <View style={styles.fab}>
            <IconButton
              iconName="Plus"
              onPress={handleCreateGroup}
              size={28}
              color={theme.colors.surface}
            />
          </View>
        </View>
      )}
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },

  groupCard: {
    marginHorizontal: 0,
    marginBottom: theme.spacing.sm,
    borderRadius: 0,
  },

  separator: {
    height: theme.spacing.sm,
  },

  fab: {
    position: 'absolute',
    bottom: theme.spacing.xl,
    right: theme.spacing.md,
    width: 56,
    height: 56,
    borderRadius: theme.radius.full,
    backgroundColor: theme.colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    ...theme.shadow.card,
  },

  chevron: {
    width: 0,
    height: 0,
  },
});
