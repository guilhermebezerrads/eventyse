export class PostService {
  addComment(comment: string, postId: string, userId: string) {
    console.log(comment, postId);
    return true;
  }

  likePost(postId: string, userId: string, liked: boolean) {
    console.log(postId);
    return true;
  }

  favoritePost(postId: string, userId: string, favorite: boolean) {
    console.log(postId);
    return true;
  }
}
