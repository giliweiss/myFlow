import { Tabs } from 'expo-router';

export default function TabsLayout() {
  return (
    <Tabs>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Groups',
          headerShown: true,
        }}
      />
    </Tabs>
  );
}
