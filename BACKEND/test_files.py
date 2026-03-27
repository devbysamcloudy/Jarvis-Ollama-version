import file_organizer

print("BEFORE organizing:")
file_organizer.list_files()

print("\n" + "=" * 50)
file_organizer.organize_by_type()

print("\n" + "=" * 50)
print("AFTER organizing:")
file_organizer.list_files()