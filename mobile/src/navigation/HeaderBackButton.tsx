import { router } from 'expo-router';
import { IconButton } from '../components/ui/IconButton';

export function HeaderBackButton() {
  return (
    <IconButton
      iconName="ChevronRight"
      onPress={() => router.back()}
    />
  );
}
