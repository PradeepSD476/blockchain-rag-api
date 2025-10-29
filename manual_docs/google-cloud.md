# Send feedbackUpload objects from a file system
This page shows you how to upload objects to your Cloud Storage bucket from your local file system. An uploaded object consists of the data you want to store along with any associated metadata. For a conceptual overview, including how to choose the optimal upload method based on your file size, see Uploads and downloads.

For instructions on uploading from memory, see Upload objects from memory.

# Required roles
To get the permissions that you need to upload objects to a bucket, ask your administrator to grant you the Storage Object User (roles/storage.objectUser) IAM role on the bucket. This predefined role contains the permissions required to upload an object to a bucket. To see the exact permissions that are required, expand the Required permissions section:

# Required permissions
If you plan on using the Google Cloud console to perform the tasks on this page, you'll also need the storage.buckets.list permission, which is not included in the Storage Object User (roles/storage.objectUser) role. To get this permission, ask your administrator to grant you the Storage Admin (roles/storage.admin) role on the project.

You can also get these permissions with other predefined roles or custom roles.

For information about granting roles on buckets, see Set and manage IAM policies on buckets.

# Upload an object to a bucket
Complete the following steps to upload an object to a bucket:


To authenticate to Cloud Storage, set up Application Default Credentials. For more information, see Set up authentication for client libraries.

The following sample uploads an individual object:



```
/**
 * TODO(developer): Uncomment the following lines before running the sample.
 */
// The ID of your GCS bucket
// const bucketName = 'your-unique-bucket-name';

// The path to your file to upload
// const filePath = 'path/to/your/file';

// The new ID for your GCS file
// const destFileName = 'your-new-file-name';

// Imports the Google Cloud client library
const {Storage} = require('@google-cloud/storage');

// Creates a client
const storage = new Storage();

async function uploadFile() {
  const options = {
    destination: destFileName,
    // Optional:
    // Set a generation-match precondition to avoid potential race conditions
    // and data corruptions. The request to upload is aborted if the object's
    // generation number does not match your precondition. For a destination
    // object that does not yet exist, set the ifGenerationMatch precondition to 0
    // If the destination object already exists in your bucket, set instead a
    // generation-match precondition using its generation number.
    preconditionOpts: {ifGenerationMatch: generationMatchPrecondition},
  };

  await storage.bucket(bucketName).upload(filePath, options);
  console.log(`${filePath} uploaded to ${bucketName}`);
}

uploadFile().catch(console.error);
The following sample uploads multiple objects concurrently:




/**
 * TODO(developer): Uncomment the following lines before running the sample.
 */
// The ID of your GCS bucket
// const bucketName = 'your-unique-bucket-name';

// The ID of the first GCS file to upload
// const firstFilePath = 'your-first-file-name';

// The ID of the second GCS file to upload
// const secondFilePath = 'your-second-file-name';

// Imports the Google Cloud client library
const {Storage, TransferManager} = require('@google-cloud/storage');

// Creates a client
const storage = new Storage();

// Creates a transfer manager client
const transferManager = new TransferManager(storage.bucket(bucketName));

async function uploadManyFilesWithTransferManager() {
  // Uploads the files
  await transferManager.uploadManyFiles([firstFilePath, secondFilePath]);

  for (const filePath of [firstFilePath, secondFilePath]) {
    console.log(`${filePath} uploaded to ${bucketName}.`);
  }
}

uploadManyFilesWithTransferManager().catch(console.error);

```
The following sample uploads all objects with a common prefix concurrently:


```

/**
 * TODO(developer): Uncomment the following lines before running the sample.
 */
// The ID of your GCS bucket
// const bucketName = 'your-unique-bucket-name';

// The local directory to upload
// const directoryName = 'your-directory';

// Imports the Google Cloud client library
const {Storage, TransferManager} = require('@google-cloud/storage');

// Creates a client
const storage = new Storage();

// Creates a transfer manager client
const transferManager = new TransferManager(storage.bucket(bucketName));

async function uploadDirectoryWithTransferManager() {
  // Uploads the directory
  await transferManager.uploadManyFiles(directoryName);

  console.log(`${directoryName} uploaded to ${bucketName}.`);
}

uploadDirectoryWithTransferManager().catch(console.error);
```
Upload the contents of a directory to a bucket
Complete the following steps to copy the contents of a directory to a bucket:

Command line
Use the gcloud storage rsync command with the --recursive flag:



gcloud storage rsync --recursive LOCAL_DIRECTORY gs://DESTINATION_BUCKET_NAME/FOLDER_NAME
Where:

LOCAL_DIRECTORY is the path to the directory that contains the files you want to upload as objects. For example, ~/my_directory.

DESTINATION_BUCKET_NAME is the name of the bucket to which you want to upload objects. For example, my-bucket.

FOLDER_NAME (optional) is the name of the folder within the bucket that you want to upload objects to. For example, my-folder.

If successful, the response looks like the following example:


Completed files 1/1 | 5.6kiB/5.6kiB
Note: You can also use cp --recursive to recursively upload directories.