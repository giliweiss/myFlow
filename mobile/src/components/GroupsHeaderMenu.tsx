import { useState } from 'react';
import { Modal, View, StyleSheet, Pressable, Text } from 'react-native';
import { useRouter } from 'expo-router';
import { IconButton } from './ui';
import { theme } from '../theme';
import { strings } from '../i18n/he';

export function GroupsHeaderMenu() {
  const router = useRouter();
  const [visible, setVisible] = useState(false);

  const openMenu = () => setVisible(true);
  const closeMenu = () => setVisible(false);

  const goToExercisesCatalog = () => {
    closeMenu();
    router.push('/exercises');
  };

  return (
    <>
      <IconButton iconName="MoreVertical" onPress={openMenu} />
      <Modal
        visible={visible}
        transparent
        animationType="fade"
        onRequestClose={closeMenu}
      >
        <Pressable style={styles.backdrop} onPress={closeMenu}>
          <View style={styles.menu}>
            <Pressable style={styles.menuItem} onPress={goToExercisesCatalog}>
              <Text style={styles.menuItemText}>{strings.exercises.catalogMenuItem}</Text>
            </Pressable>
          </View>
        </Pressable>
      </Modal>
    </>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.35)',
    justifyContent: 'flex-start',
    alignItems: 'flex-start',
    paddingTop: 56,
    paddingHorizontal: theme.spacing.md,
  },

  menu: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radius.md,
    minWidth: 200,
    overflow: 'hidden',
    ...theme.shadow.card,
  },

  menuItem: {
    paddingVertical: theme.spacing.md,
    paddingHorizontal: theme.spacing.lg,
  },

  menuItemText: {
    ...theme.typography.body,
    color: theme.colors.textPrimary,
    textAlign: 'right',
  },
});
